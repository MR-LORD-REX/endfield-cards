"""Build and verify wheel/sdist resources, then install into fresh local targets.

The installed dependency environment is reused, while the cards package itself is
installed with --no-deps into new, isolated targets. No reference checkout is put
on sys.path. Artifacts and machine-readable results stay in cards/local/.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from email.parser import Parser
from pathlib import Path, PurePosixPath
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
RESOURCE_PREFIX = "endfield_cards/assets/resources/"
FORBIDDEN_PARTS = {"design-data", "previews", "staging", "akef_cards", "endfield-cards", "local"}


def _check_names(names: list[str]) -> None:
    for name in names:
        parts = set(PurePosixPath(name).parts)
        if FORBIDDEN_PARTS & parts:
            raise ValueError(f"Private or reference material included in package: {name}")


def verify_wheel(path: Path) -> dict[str, Any]:
    """Inspect complete resource hashes, notices, package typing, and dependencies."""
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        _check_names(names)
        metadata_name = next(name for name in names if name.endswith(".dist-info/METADATA"))
        metadata = Parser().parsestr(archive.read(metadata_name).decode("utf-8"))
        requirements = metadata.get_all("Requires-Dist", [])
        if any(requirement.lower().startswith(("endfield-py", "akef")) for requirement in requirements):
            raise ValueError("Replacement package depends on a legacy reference SDK")
        if not any(requirement.lower().startswith("skport-py") for requirement in requirements):
            raise ValueError("Package metadata omits skport-py")
        if "endfield_cards/py.typed" not in names:
            raise ValueError("Typed package marker missing")
        document = json.loads(archive.read(RESOURCE_PREFIX + "manifest.json"))
        resource_bytes = 0
        for key, spec in document["assets"].items():
            data = archive.read(RESOURCE_PREFIX + spec["path"])
            if len(data) != spec["bytes"] or hashlib.sha256(data).hexdigest() != spec["sha256"]:
                raise ValueError(f"Packaged resource checksum mismatch: {key}")
            resource_bytes += len(data)
        expected_locales = {
            f"endfield_cards/i18n/locales/{locale}.json"
            for locale in ("en", "ja", "ko", "zh-Hans", "zh-Hant")
        }
        if not expected_locales.issubset(names):
            raise ValueError("One or more localization catalogs missing from wheel")
        return {
            "name": metadata["Name"],
            "version": metadata["Version"],
            "requires_python": metadata["Requires-Python"],
            "requirements": requirements,
            "resources": len(document["assets"]),
            "aliases": len(document["aliases"]),
            "resource_bytes": resource_bytes,
            "wheel_bytes": path.stat().st_size,
        }


def verify_sdist(path: Path) -> dict[str, Any]:
    """Check the sdist contains the complete resource set without private inputs."""
    with tarfile.open(path, "r:gz") as archive:
        members = {member.name: member for member in archive.getmembers()}
        _check_names(list(members))
        manifest_name = next(
            name for name in members if name.endswith("/src/" + RESOURCE_PREFIX + "manifest.json")
        )
        prefix = manifest_name.removesuffix("manifest.json")
        manifest_stream = archive.extractfile(manifest_name)
        if manifest_stream is None:
            raise ValueError("Sdist manifest is not a regular file")
        document = json.load(manifest_stream)
        for key, spec in document["assets"].items():
            stream = archive.extractfile(prefix + spec["path"])
            if stream is None:
                raise ValueError(f"Sdist resource missing: {key}")
            data = stream.read()
            if len(data) != spec["bytes"] or hashlib.sha256(data).hexdigest() != spec["sha256"]:
                raise ValueError(f"Sdist resource checksum mismatch: {key}")
        return {"resources": len(document["assets"]), "sdist_bytes": path.stat().st_size}


def _run(command: list[str], *, cwd: Path) -> str:
    result = subprocess.run(
        command, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False
    )
    if result.returncode:
        raise RuntimeError("Command failed: " + " ".join(command) + "\n" + result.stdout + result.stderr)
    return result.stdout


def _install_smoke(wheel: Path, target: Path) -> dict[str, Any]:
    _run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--no-deps",
            "--no-compile",
            "--target",
            str(target),
            str(wheel),
        ],
        cwd=PROJECT,
    )
    code = """
import json, pathlib, sys
target = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(target))
import endfield_cards
assert endfield_cards.EF_Cards.__name__ == "EF_Cards"
assert endfield_cards.Cards is endfield_cards.EF_Cards
from endfield_cards.assets.manifest import Manifest
from endfield_cards.assets.fonts import FontManager
from PIL import Image
assert pathlib.Path(endfield_cards.__file__).resolve().is_relative_to(target)
manifest = Manifest()
for key in manifest.keys:
    resource = manifest.path(key)
    assert resource.resolve().is_relative_to(target)
    if manifest.entries[key]['media_type'] == 'image/png':
        with Image.open(resource) as image:
            image.load()
fonts = FontManager(limit=8)
for locale, text in [('en', 'Endfield'), ('ja', '\\u30c6\\u30b9\\u30c8'), ('ko', '\\ud14c\\uc2a4\\ud2b8'),
                     ('zh-Hans', '\\u6d4b\\u8bd5'), ('zh-Hant', '\\u6e2c\\u8a66')]:
    assert fonts.get(24, locale=locale, text=text).getlength(text) > 0
assert not any(name == 'endfield' or name.startswith(('endfield.', 'akef.', 'akef_cards.')) for name in sys.modules)
print(json.dumps({'package_file': endfield_cards.__file__, 'resources': len(manifest.keys),
                  'font_locales': 5, 'legacy_modules_loaded': False}))
"""
    output = _run([sys.executable, "-I", "-c", code, str(target)], cwd=target)
    return json.loads(output)


def verify(output: Path) -> dict[str, Any]:
    """Build both formats and smoke-test installs from wheel and sdist."""
    output.mkdir(parents=True, exist_ok=True)
    run_directory = Path(tempfile.mkdtemp(prefix="run-", dir=output))
    distribution = run_directory / "dist"
    print("Building wheel and sdist...", flush=True)
    _run(
        [sys.executable, "-m", "build", "--no-isolation", "--outdir", str(distribution), str(PROJECT)],
        cwd=PROJECT,
    )
    wheel = next(distribution.glob("*.whl"))
    sdist = next(distribution.glob("*.tar.gz"))
    results: dict[str, Any] = {
        "run_directory": str(run_directory),
        "wheel": verify_wheel(wheel),
        "sdist": verify_sdist(sdist),
    }
    print("Checking isolated wheel install...", flush=True)
    results["wheel_install"] = _install_smoke(wheel, run_directory / "wheel-install")
    rebuilt = run_directory / "from-sdist"
    print("Building and installing from sdist...", flush=True)
    _run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--no-deps",
            "--no-build-isolation",
            "--wheel-dir",
            str(rebuilt),
            str(sdist),
        ],
        cwd=PROJECT,
    )
    sdist_wheel = next(rebuilt.glob("*.whl"))
    results["sdist_wheel"] = verify_wheel(sdist_wheel)
    results["sdist_install"] = _install_smoke(sdist_wheel, run_directory / "sdist-install")
    results["passed"] = True
    result_path = run_directory / "verification.json"
    result_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    (output / "latest.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=PROJECT / "local/package-check")
    args = parser.parse_args()
    results = verify(args.output.resolve())
    print(f"Packaging verified: {results['wheel']['resources']} resources; {results['run_directory']}")


if __name__ == "__main__":
    main()

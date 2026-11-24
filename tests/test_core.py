from __future__ import annotations

import io
import logging
import os
import subprocess
import sys
from pathlib import Path

import pytest
from PIL import Image

from endfield_cards.cache import cache_key
from endfield_cards.config import CacheConfig, CardsConfig, DownloadConfig, OutputConfig
from endfield_cards.errors import DataValidationError, EncodingError
from endfield_cards.logging import RedactingFormatter, configure_logging, redact
from endfield_cards.models import CardResult, OwnerIdentity, RenderContext
from endfield_cards.rendering.encoding import encode


@pytest.mark.parametrize("name,uid", [("", "123"), ("name", ""), (None, "123"), ("name", None)])
def test_owner_requires_actual_name_and_game_uid(name: object, uid: object) -> None:
    with pytest.raises(DataValidationError):
        OwnerIdentity(name, uid)


def test_context_requires_typed_owner_and_keys_isolate_accounts() -> None:
    with pytest.raises(DataValidationError):
        RenderContext(owner=None)
    first = RenderContext(OwnerIdentity("One", "10001", "social-1"))
    second = RenderContext(OwnerIdentity("Two", "10002", "social-2"))
    same_data = {"operator": "char_0001", "level": 20}
    assert cache_key("character", same_data, first) != cache_key("character", same_data, second)
    assert cache_key("character", same_data, first) != cache_key("character", same_data, first.owner)


@pytest.mark.parametrize(
    "value",
    [
        "Bearer bearer_secret_opaque",
        "Authorization: Bearer bearer_secret_opaque",
        "Authorization: Basic basic_secret_opaque",
        '{"token": "json_secret_opaque"}',
        "{'token': 'repr_secret_opaque'}",
        "url=https://user:password_opaque@example.test/asset.png?signature=signed_secret_opaque#private",
        "Cookie: session=cookie_secret_opaque; preference=other_cookie_secret_opaque",
    ],
)
def test_redaction_covers_credentials_in_text(value: str) -> None:
    output = str(redact(value))
    for secret in (
        "bearer_secret_opaque",
        "json_secret_opaque",
        "repr_secret_opaque",
        "password_opaque",
        "signed_secret_opaque",
        "basic_secret_opaque",
        "cookie_secret_opaque",
        "other_cookie_secret_opaque",
    ):
        assert secret not in output


def test_structured_redaction_includes_sdk_credential_field() -> None:
    output = redact(
        {"cred": "skport_credential_opaque", "nested": [{"token": "nested_secret"}], "name": "safe"}
    )
    assert output == {"cred": "[redacted]", "nested": [{"token": "[redacted]"}], "name": "safe"}


def test_configured_logging_is_opt_in_and_redacts_args_and_exception() -> None:
    root = logging.getLogger()
    original_root = (root.level, tuple(root.handlers), tuple(root.filters))
    logger = logging.getLogger("endfield_cards")
    original_library = (logger.level, list(logger.handlers), logger.propagate)
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    try:
        configure_logging(logging.DEBUG, handler=handler)
        configure_logging(logging.DEBUG, handler=handler)
        assert len([item for item in logger.handlers if getattr(item, "_endfield_cards_owned", False)]) == 1
        logger.info("payload=%s", {"token": "structured_secret_opaque", "name": "safe-name"})
        try:
            raise ValueError("Authorization: Bearer exception_secret_opaque")
        except ValueError:
            logger.exception("could not fetch https://example.test/a.png?token=url_secret_opaque")
        text = stream.getvalue()
        assert "safe-name" in text
        assert all(
            secret not in text
            for secret in ("structured_secret_opaque", "exception_secret_opaque", "url_secret_opaque")
        )
        assert (root.level, tuple(root.handlers), tuple(root.filters)) == original_root
    finally:
        logger.handlers[:] = original_library[1]
        logger.setLevel(original_library[0])
        logger.propagate = original_library[2]
        handler.close()


def test_formatter_does_not_mutate_caller_payload() -> None:
    original = {"token": "caller_secret_opaque", "visible": "yes"}
    record = logging.LogRecord("endfield_cards", logging.INFO, "", 1, "%s", (original,), None)
    output = RedactingFormatter("%(message)s").format(record)
    assert "caller_secret_opaque" not in output
    assert original == {"token": "caller_secret_opaque", "visible": "yes"}


@pytest.mark.parametrize(
    "config",
    [
        lambda: CacheConfig(decoded_bytes=-1),
        lambda: CacheConfig(ttl_seconds=-1),
        lambda: DownloadConfig(concurrency=0),
        lambda: DownloadConfig(max_pixels=0),
        lambda: DownloadConfig(max_redirects=-1),
        lambda: CardsConfig(admitted_jobs=0),
        lambda: OutputConfig(format="PDF"),
        lambda: OutputConfig(max_bytes=0),
    ],
)
def test_invalid_resource_budgets_are_rejected(config: object) -> None:
    with pytest.raises(ValueError):
        config()


@pytest.mark.parametrize("format", ["PNG", "JPEG", "WEBP"])
def test_output_encoding_and_budget_preserve_caller_pixels(format: str) -> None:
    image = Image.new("RGBA", (20, 20), (120, 30, 10, 150))
    original_pixels = image.tobytes()
    encoded = encode(image, OutputConfig(format=format))
    with Image.open(io.BytesIO(encoded)) as result:
        assert result.format == format and result.size == image.size
    assert image.tobytes() == original_pixels
    with pytest.raises(EncodingError) as exc:
        encode(image, OutputConfig(format=format, max_bytes=1))
    assert exc.value.code == "output_budget_exceeded"


def test_result_image_copy_and_atomic_save_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    data = encode(Image.new("RGBA", (8, 8), "red"), OutputConfig())
    result = CardResult(data, "PNG", 8, 8, "character", "field")
    pixels = result.to_pillow()
    pixels.putpixel((0, 0), (0, 0, 0, 0))
    assert result.to_pillow().getpixel((0, 0)) == (255, 0, 0, 255)
    target = tmp_path / "result.png"
    result.save(target)
    assert target.read_bytes() == data

    def rejected_replace(source: object, destination: object) -> None:
        raise PermissionError("target is locked")

    monkeypatch.setattr("endfield_cards.models.result.os.replace", rejected_replace)
    with pytest.raises(PermissionError):
        result.save(target)
    assert target.read_bytes() == data
    assert list(tmp_path.iterdir()) == [target]


def test_pure_package_import_does_not_create_sessions_or_write_files(tmp_path: Path) -> None:
    source = Path(__file__).resolve().parents[1] / "src"
    sdk = source.parents[1] / "skport-py" / "src"
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join((str(source), str(sdk)))
    script = """
import aiohttp
import logging
import os
import pathlib
import socket

root = logging.getLogger()
original = (root.level, tuple(root.handlers))
def forbidden(*args, **kwargs):
    raise AssertionError("package import attempted an external side effect")
aiohttp.ClientSession.__init__ = forbidden
socket.create_connection = forbidden
socket.socket.connect = forbidden
pathlib.Path.mkdir = forbidden
pathlib.Path.write_text = forbidden
pathlib.Path.write_bytes = forbidden
os.mkdir = forbidden
os.makedirs = forbidden
import endfield_cards
assert hasattr(endfield_cards, "Cards")
assert (root.level, tuple(root.handlers)) == original
"""
    checked = subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert checked.returncode == 0, checked.stderr
    assert list(tmp_path.iterdir()) == []

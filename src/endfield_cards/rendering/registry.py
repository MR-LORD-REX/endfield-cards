"""Named variants and lazy imports; discovery does not render or fetch."""

from importlib import import_module
from types import MappingProxyType, ModuleType

from endfield_cards.errors import CardNotImplementedError, UnsupportedVariantError

VARIANTS = MappingProxyType(
    {
        "profile": ("overview", "operations", "identity"),
        "character": ("field", "dossier", "terminal", "portrait"),
        **{
            name: ("light", "dark")
            for name in (
                "roster",
                "activity",
                "factory",
                "exploration",
                "monument",
                "monument_detail",
                "contingency_contract",
                "contingency_contract_detail",
                "pulls",
                "wiki",
            )
        },
    }
)
ALIASES = MappingProxyType(
    {
        "all_characters": "roster",
        "live": "activity",
        "monument_event": "monument_detail",
        "monument_detailed": "monument_detail",
        "contract": "contingency_contract",
        "contract_detail": "contingency_contract_detail",
        "contingency_contract_detailed": "contingency_contract_detail",
    }
)

# Generic text exporters are retained internally, but are not finished card layouts.
UNIMPLEMENTED = frozenset({"wiki"})


def ensure_implemented(family: str, variant: str) -> None:
    """Reject unfinished layouts before SDK, image downloads or worker admission."""
    family = ALIASES.get(family, family)
    if family in UNIMPLEMENTED:
        name = {
            "monument_detail": "monument_detailed",
            "contingency_contract_detail": "contingency_contract_detailed",
        }.get(family, family)
        template = VARIANTS[family].index(variant) + 1
        raise CardNotImplementedError(f"{name}_card(template={template}) is not implemented yet")


def pick(family: str, variant: str | None = None) -> tuple[str, str, ModuleType]:
    family = ALIASES.get(family, family)
    if family not in VARIANTS:
        raise UnsupportedVariantError(f"unknown card family {family!r}", code="unsupported_family")
    selected = variant or VARIANTS[family][0]
    if selected not in VARIANTS[family]:
        raise UnsupportedVariantError(f"unknown {family} variant {selected!r}; choose {VARIANTS[family]}")
    ensure_implemented(family, selected)
    return family, selected, import_module(f"endfield_cards.rendering.templates.{family}")

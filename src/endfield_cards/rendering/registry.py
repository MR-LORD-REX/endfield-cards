"""Named variants and lazy imports; discovery does not render or fetch."""

from importlib import import_module
from types import MappingProxyType, ModuleType

from endfield_cards.errors import UnsupportedVariantError

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
        "live": "activity",
        "monument_event": "monument_detail",
        "monument_detailed": "monument_detail",
        "contract": "contingency_contract",
        "contract_detail": "contingency_contract_detail",
    }
)


def pick(family: str, variant: str | None = None) -> tuple[str, str, ModuleType]:
    family = ALIASES.get(family, family)
    if family not in VARIANTS:
        raise UnsupportedVariantError(f"unknown card family {family!r}", code="unsupported_family")
    selected = variant or VARIANTS[family][0]
    if selected not in VARIANTS[family]:
        raise UnsupportedVariantError(f"unknown {family} variant {selected!r}; choose {VARIANTS[family]}")
    return family, selected, import_module(f"endfield_cards.rendering.templates.{family}")

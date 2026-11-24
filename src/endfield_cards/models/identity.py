"""The in-game identity printed on every page."""

from dataclasses import dataclass

from endfield_cards.errors import DataValidationError


@dataclass(frozen=True)
class OwnerIdentity:
    name: str
    game_uid: str
    skport_id: str | None = None

    def __post_init__(self) -> None:
        if (
            not isinstance(self.name, str)
            or not self.name.strip()
            or self.game_uid is None
            or isinstance(self.game_uid, bool)
            or not str(self.game_uid).strip()
        ):
            raise DataValidationError("an in-game name and game UID are required")
        object.__setattr__(self, "game_uid", str(self.game_uid))

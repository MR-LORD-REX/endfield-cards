"""Shared Endfield typography, semantic icons, artwork and identity panels."""

from datetime import UTC
from typing import Any
from zoneinfo import ZoneInfo

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

from endfield_cards.assets.fonts import FontManager
from endfield_cards.assets.manifest import resource_path
from endfield_cards.errors import AssetError
from endfield_cards.i18n import t
from endfield_cards.models import Artwork, RenderContext

STAT_ICONS = {
    1: "MaxHp",
    2: "Atk",
    3: "Def",
    9: "CriticalRate",
    10: "CriticalDamageIncrease",
    39: "Str",
    40: "Agi",
    41: "Wisd",
    42: "Will",
    44: "UltimateSpGainScalar",
    50: "PhysicalDamageIncrease",
    51: "FireDamageIncrease",
    52: "PulseDamageIncrease",
    53: "CrystDamageIncrease",
    54: "NaturalDamageIncrease",
}
ELEMENT_COLORS = {
    "pulse": "#A584E8",
    "electric": "#A584E8",
    "fire": "#E87854",
    "heat": "#E87854",
    "cryst": "#5CB9D9",
    "cryo": "#5CB9D9",
    "natural": "#90B867",
    "nature": "#90B867",
}
_FONTS = FontManager(limit=64)


def element_key(model: object) -> str:
    return getattr(getattr(model, "element", None), "key", "").removeprefix("char_property_").lower()


def art_url(model: object) -> str | None:
    images = getattr(model, "images", None)
    if images is None:
        return None
    for key in ("half_body", "splash", "portrait", "avatar"):
        link = getattr(images, key, None)
        if link is not None and link.url:
            return link.url
    return None


def wrap_text(draw: ImageDraw.ImageDraw, value: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    """Measure both spaced and unspaced scripts; retain all source text."""
    lines: list[str] = []
    for paragraph in str(value).split("\n"):
        current = ""
        for char in paragraph:
            if current and draw.textlength(current + char, font=font) > width:
                split = current.rfind(" ")
                if split > len(current) // 2:
                    lines.append(current[:split])
                    current = current[split + 1 :] + char
                else:
                    lines.append(current)
                    current = char
            else:
                current += char
        lines.append(current)
    return lines


class PageCanvas:
    """A single bounded page with a reserved owner/watermark footer."""

    def __init__(
        self,
        title: str,
        context: RenderContext,
        *,
        dark: bool = False,
        size: tuple[int, int] = (1600, 1000),
        assets: dict[str, Image.Image] | None = None,
        header: bool = True,
    ) -> None:
        self.context = context
        self.dark = dark
        self.width, self.height = size
        self.background = "#181B20" if dark else "#F2F1EC"
        self.fg = "#F4F3EE" if dark else "#22252B"
        self.muted = "#A0A5AF" if dark else "#656B76"
        self.accent = "#FFC800"
        self.panel_color = "#242931" if dark else "#FCFBF8"
        self.line = "#3A414C" if dark else "#D6D5CE"
        self.assets = assets if assets is not None else {}
        self.fonts = _FONTS
        self.image = Image.new("RGBA", size, self.background)
        self.draw = ImageDraw.Draw(self.image)
        if header:
            self.draw.rectangle((0, 0, 12, self.height), fill=self.accent)
            self.text(42, 24, "ENDFIELD / " + self.t(title), size=18, fill=self.muted, bold=True)
            self.text(42, 51, self.t(title), size=46, bold=True, width=self.width - 300, max_lines=1)
            self.draw.line((42, 120, self.width - 42, 120), fill=self.line, width=2)

    def t(self, key: str, **values: object) -> str:
        return t(key, self.context.locale, **values)

    def text(
        self,
        x: int,
        y: int,
        value: object,
        *,
        size: int = 24,
        fill: Any = None,
        bold: bool = False,
        width: int | None = None,
        max_lines: int | None = None,
    ) -> int:
        text = str(value)
        font = self.fonts.get(
            size, weight="semibold" if bold else "regular", locale=self.context.locale, text=text
        )
        lines = wrap_text(self.draw, text, font, width) if width else text.split("\n")
        if max_lines is not None and len(lines) > max_lines:
            while size > 14 and len(lines) > max_lines:
                size -= 1
                font = self.fonts.get(
                    size, weight="semibold" if bold else "regular", locale=self.context.locale, text=text
                )
                lines = wrap_text(self.draw, text, font, width or self.width - x - 42)
            if len(lines) > max_lines:
                lines = lines[:max_lines]
                last = lines[-1]
                while last and self.draw.textlength(last + "…", font=font) > (width or self.width - x - 42):
                    last = last[:-1]
                lines[-1] = last + "…"
        line_height = size + 8
        for index, line in enumerate(lines):
            self.draw.text((x, y + index * line_height), line, font=font, fill=fill or self.fg)
        return len(lines) * line_height

    def panel(self, box: tuple[int, int, int, int]) -> None:
        self.draw.rounded_rectangle(box, radius=12, fill=self.panel_color, outline=self.line, width=1)

    def scrim(self, box: tuple[int, int, int, int], *, dark: bool = True, alpha: int = 220) -> None:
        x, y, right, bottom = box
        layer = Image.new(
            "RGBA", (right - x, bottom - y), (17, 22, 29, alpha) if dark else (252, 251, 248, alpha)
        )
        self.image.alpha_composite(layer, (x, y))

    def section(self, title: str, x: int, y: int, width: int) -> int:
        self.draw.rectangle((x, y + 5, x + 4, y + 27), fill=self.accent)
        height = self.text(x + 14, y, self.t(title), size=23, bold=True, width=width - 14)
        self.draw.line((x, y + height + 6, x + width, y + height + 6), fill=self.line, width=1)
        return height + 20

    def row(
        self, label: str, value: object, x: int, y: int, width: int = 450, icon: str | None = None
    ) -> int:
        if icon:
            self.icon(icon, x, y + 1, 26)
        offset = 36 if icon else 0
        lh = self.text(
            x + offset, y, self.t(label), size=22, fill=self.muted, width=int(width * 0.63) - offset
        )
        rh = self.text(x + int(width * 0.66), y, value, size=25, bold=True, width=int(width * 0.34))
        height = max(lh, rh) + 15
        self.draw.line((x, y + height - 5, x + width, y + height - 5), fill=self.line, width=1)
        return height

    def icon(self, key: str, x: int, y: int, size: int = 32, *, tint: str | None = None) -> bool:
        source = self.assets.get(key)
        if source is None:
            try:
                with Image.open(resource_path(key)) as original:
                    source = original.convert("RGBA")
            except (AssetError, OSError, KeyError):
                return False
        glyph = ImageOps.contain(source.convert("RGBA"), (size, size), Image.Resampling.LANCZOS)
        if tint is not None or (
            key.startswith(("stat.", "profession.", "weapon.", "player.", "rarity."))
            and key
            not in {
                "player.monument-event",
                "player.monument-detailed",
                "player.monument_detail",
            }
        ):
            alpha = glyph.getchannel("A")
            if alpha.getextrema() != (255, 255):
                glyph = Image.new("RGBA", glyph.size, tint or self.fg)
                glyph.putalpha(alpha)
        self.image.alpha_composite(glyph, (x + (size - glyph.width) // 2, y + (size - glyph.height) // 2))
        return True

    def finish(self, page: int = 1, pages: int = 1) -> Image.Image:
        y = self.height - 66
        self.draw.rectangle((0, y, self.width, self.height), fill="#11151B")
        owners = [self.context.owner]
        if self.context.comparison_owner is not None:
            owners.append(self.context.comparison_owner)
        available = self.width - 500
        cell = available // len(owners)
        for index, owner in enumerate(owners):
            x = 42 + index * cell
            self.text(x, y + 5, owner.name, size=21, fill="#F4F3EE", bold=True, width=cell - 24, max_lines=1)
            self.text(
                x, y + 32, f"UID {owner.game_uid}", size=16, fill="#CDD2DA", width=cell - 24, max_lines=1
            )
        self.text(self.width - 446, y + 9, "akef-cards · endfield-cards", size=20, fill="#FFC800")
        stamp = self.context.snapshot_at
        meta = f"{page:02d} / {pages:02d}"
        if stamp is not None:
            if stamp.tzinfo is None:
                stamp = stamp.replace(tzinfo=UTC)
            stamp = stamp.astimezone(ZoneInfo(self.context.display_timezone))
            meta += "   ·   " + stamp.strftime("%Y-%m-%d %H:%M %Z")
        self.text(self.width - 446, y + 38, meta, size=13, fill="#A0A5AF", width=400, max_lines=1)
        return self.image


def place_art(
    canvas: PageCanvas,
    source: Image.Image | None,
    box: tuple[int, int, int, int],
    artwork: Artwork | None = None,
    *,
    blend: bool = False,
) -> None:
    """Copy, crop around the focal point, and shade art within its own region."""
    x, y, right, bottom = box
    width, height = right - x, bottom - y
    if source is None:
        canvas.draw.ellipse((x + 20, y + 80, right - 20, bottom - 50), outline=canvas.line, width=2)
        canvas.text(x + 40, y + height // 2, canvas.t("Unavailable"), fill=canvas.muted, width=width - 80)
        return
    pixels = ImageOps.exif_transpose(source).convert("RGBA")
    if artwork is None or artwork.fit == "contain":
        if artwork is None:
            bounds = pixels.getchannel("A").getbbox()
            if bounds:
                pixels = pixels.crop(bounds)
        fitted = ImageOps.contain(pixels, (width, height), Image.Resampling.LANCZOS)
        layer = Image.new("RGBA", (width, height))
        layer.alpha_composite(fitted, ((width - fitted.width) // 2, (height - fitted.height) // 2))
    else:
        focus = artwork.focal_point if artwork else (0.5, 0.35)
        layer = ImageOps.fit(pixels, (width, height), Image.Resampling.LANCZOS, centering=focus)
    if blend:
        mask = Image.new("L", layer.size, 255)
        md = ImageDraw.Draw(mask)
        edge = min(100, width // 5)
        content = layer.getchannel("A").getbbox() or (0, 0, width, height)
        left_edge, _, right_edge, bottom_edge = content
        for i in range(edge):
            alpha = int(255 * i / edge)
            md.line((left_edge + i, 0, left_edge + i, height), fill=alpha)
            md.line((right_edge - 1 - i, 0, right_edge - 1 - i, height), fill=alpha)
        fade = min(90, height // 5)
        for i in range(fade):
            md.line((0, bottom_edge - 1 - i, width, bottom_edge - 1 - i), fill=int(255 * i / fade))
        layer.putalpha(ImageChops.multiply(layer.getchannel("A"), mask))
        shadow = Image.new("RGBA", layer.size, "#080D18")
        shadow.putalpha(layer.getchannel("A").point(lambda a: a // 3))
        canvas.image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(16)), (x + 10, y + 10))
    canvas.image.alpha_composite(layer, (x, y))

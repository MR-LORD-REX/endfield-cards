"""Stable errors at rendering, asset and SDK boundaries."""


class CardError(Exception):
    """Base error with a stable machine-readable code and preserved cause."""

    default_code = "card_error"

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.code = code or self.default_code


class DataValidationError(CardError):
    default_code = "invalid_data"


class OwnerMismatchError(DataValidationError):
    default_code = "owner_mismatch"


class UnsupportedVariantError(DataValidationError):
    default_code = "unsupported_variant"


class AssetError(CardError):
    default_code = "asset_error"


class DownloadError(AssetError):
    default_code = "download_failed"


class ImageDecodeError(AssetError):
    default_code = "image_decode_failed"


class CacheError(CardError):
    default_code = "cache_error"


class ResourceClosedError(CardError):
    default_code = "resource_closed"


class EncodingError(CardError):
    default_code = "encoding_failed"


class RenderError(CardError):
    default_code = "render_failed"


class FetchError(CardError):
    default_code = "fetch_failed"


class CardNotImplementedError(CardError, NotImplementedError):
    """A planned card/template has no finished renderer yet."""

    default_code = "not_implemented"

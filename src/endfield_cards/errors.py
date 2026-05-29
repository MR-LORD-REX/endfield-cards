# Copyright (c) 2026 MR-LORD-REX
# All rights reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

"""
Error handling and custom exceptions for Endfield Cards.

This module defines error classes for different failure scenarios:
- CardBuildError: Critical errors during card building (whole card fails)
- ComponentBuildError: Non-critical errors during component building (continue with degraded quality)
- AssetError: Asset loading failures
- DataFetchError: External data fetch failures
- RenderError: Image rendering failures
- ValidationError: Data validation failures
"""

import logging
from typing import Optional
from enum import Enum


class ErrorSeverity(Enum):
    """Error severity levels."""
    CRITICAL = "CRITICAL"  # Whole card build fails
    WARNING = "WARNING"    # Component fails but card can continue
    INFO = "INFO"          # Non-blocking issues


logger = logging.getLogger(__name__)


class EndfieldCardError(Exception):
    """Base exception for all Endfield Card errors."""
    
    def __init__(
        self,
        message: str,
        error_code: str = "UNKNOWN_ERROR",
        severity: ErrorSeverity = ErrorSeverity.CRITICAL,
        context: Optional[dict] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.severity = severity
        self.context = context or {}
        super().__init__(self.format_message())

    def format_message(self) -> str:
        """Format error message with context."""
        msg = f"[{self.error_code}] {self.message}"
        if self.context:
            msg += f" | Context: {self.context}"
        return msg

    def log(self):
        """Log error with appropriate level based on severity."""
        if self.severity == ErrorSeverity.CRITICAL:
            logger.error(self.format_message(), exc_info=True)
        elif self.severity == ErrorSeverity.WARNING:
            logger.warning(self.format_message())
        else:
            logger.info(self.format_message())


class CardBuildError(EndfieldCardError):
    """
    Critical error during card building.
    Raised when the whole card build fails and cannot continue.
    """

    def __init__(
        self,
        message: str,
        card_type: str = "UNKNOWN",
        uid: Optional[int] = None,
        original_error: Optional[Exception] = None,
        context: Optional[dict] = None,
    ):
        ctx = context or {}
        ctx.update({"card_type": card_type, "uid": uid})
        super().__init__(
            message=message,
            error_code="CARD_BUILD_FAILED",
            severity=ErrorSeverity.CRITICAL,
            context=ctx,
        )
        self.card_type = card_type
        self.uid = uid
        self.original_error = original_error


class ComponentBuildError(EndfieldCardError):
    """
    Non-critical error during component building.
    Logged but card continues to build with degraded quality.
    """

    def __init__(
        self,
        message: str,
        component_name: str = "UNKNOWN",
        original_error: Optional[Exception] = None,
        context: Optional[dict] = None,
    ):
        ctx = context or {}
        ctx.update({"component": component_name})
        super().__init__(
            message=message,
            error_code="COMPONENT_BUILD_FAILED",
            severity=ErrorSeverity.WARNING,
            context=ctx,
        )
        self.component_name = component_name
        self.original_error = original_error


class AssetError(ComponentBuildError):
    """Error loading or processing assets."""

    def __init__(
        self,
        message: str,
        asset_name: str = "UNKNOWN",
        original_error: Optional[Exception] = None,
        context: Optional[dict] = None,
    ):
        ctx = context or {}
        ctx.update({"asset": asset_name})
        super().__init__(
            message=message,
            component_name=f"AssetLoader[{asset_name}]",
            original_error=original_error,
            context=ctx,
        )
        self.asset_name = asset_name


class DataFetchError(ComponentBuildError):
    """Error fetching external data (API calls, etc.)."""

    def __init__(
        self,
        message: str,
        data_source: str = "UNKNOWN",
        uid: Optional[int] = None,
        original_error: Optional[Exception] = None,
        context: Optional[dict] = None,
    ):
        ctx = context or {}
        ctx.update({"data_source": data_source, "uid": uid})
        super().__init__(
            message=message,
            component_name=f"DataFetcher[{data_source}]",
            original_error=original_error,
            context=ctx,
        )
        self.data_source = data_source
        self.uid = uid


class RenderError(ComponentBuildError):
    """Error during image rendering or compositing."""

    def __init__(
        self,
        message: str,
        component_name: str = "UNKNOWN",
        original_error: Optional[Exception] = None,
        context: Optional[dict] = None,
    ):
        ctx = context or {}
        super().__init__(
            message=message,
            component_name=f"Renderer[{component_name}]",
            original_error=original_error,
            context=ctx,
        )


class ValidationError(ComponentBuildError):
    """Error validating data or structure."""

    def __init__(
        self,
        message: str,
        validation_type: str = "UNKNOWN",
        original_error: Optional[Exception] = None,
        context: Optional[dict] = None,
    ):
        ctx = context or {}
        ctx.update({"validation": validation_type})
        super().__init__(
            message=message,
            component_name=f"Validator[{validation_type}]",
            original_error=original_error,
            context=ctx,
        )
        self.validation_type = validation_type


class ComponentBuildResult:
    """
    Result wrapper for component building with error handling.
    Allows components to fail gracefully without crashing the whole card.
    """

    def __init__(
        self,
        success: bool,
        data: Optional[object] = None,
        error: Optional[ComponentBuildError] = None,
        component_name: str = "UNKNOWN",
    ):
        self.success = success
        self.data = data
        self.error = error
        self.component_name = component_name

    @classmethod
    def ok(cls, data: object, component_name: str = "UNKNOWN") -> "ComponentBuildResult":
        """Create a successful result."""
        return cls(success=True, data=data, component_name=component_name)

    @classmethod
    def fail(
        cls,
        error: ComponentBuildError,
        component_name: str = "UNKNOWN",
    ) -> "ComponentBuildResult":
        """Create a failed result."""
        return cls(success=False, error=error, component_name=component_name)

    def __bool__(self) -> bool:
        """Check if result is successful."""
        return self.success

    def unwrap_or(self, default: object) -> object:
        """Get data or return default value."""
        return self.data if self.success else default

    def log_if_failed(self):
        """Log error if this result is a failure."""
        if not self.success and self.error:
            self.error.log()

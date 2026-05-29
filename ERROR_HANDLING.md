# Error Handling System

## Overview

The Endfield Cards package includes a comprehensive error handling system that distinguishes between critical errors (that fail the entire card build) and non-critical errors (that fail individual components but allow the build to continue).

## Error Classes

### Error Hierarchy

```
EndfieldCardError (Base)
├── CardBuildError (CRITICAL)
│   └── Raised when the whole card build fails
├── ComponentBuildError (WARNING)
│   ├── AssetError
│   ├── DataFetchError
│   ├── RenderError
│   └── ValidationError
```

### Error Classes

#### `EndfieldCardError`
Base exception for all Endfield Card errors. All custom exceptions inherit from this.

**Attributes:**
- `message`: Error message
- `error_code`: Error code identifier (e.g., "CARD_BUILD_FAILED")
- `severity`: Error severity (CRITICAL, WARNING, INFO)
- `context`: Dictionary with additional context information

**Methods:**
- `format_message()`: Returns formatted error message with context
- `log()`: Logs error with appropriate level based on severity

#### `CardBuildError`
**Severity:** CRITICAL

Raised when the entire card build fails and cannot continue. This includes:
- Critical component failures (e.g., main frame rendering)
- External data fetch failures that prevent card building
- Validation failures for essential data

**Constructor:**
```python
CardBuildError(
    message: str,
    card_type: str = "UNKNOWN",
    uid: Optional[int] = None,
    original_error: Optional[Exception] = None,
    context: Optional[dict] = None
)
```

**Example:**
```python
try:
    char_data = await self.ef.get_character_showcase(uid, char_index)
except Exception as e:
    raise CardBuildError(
        message="Failed to fetch character showcase data",
        card_type="character",
        uid=uid,
        original_error=e,
        context={"char_index": char_index}
    )
```

#### `ComponentBuildError`
**Severity:** WARNING

Raised when a non-critical component fails. The card build continues with degraded quality. This includes:
- Missing assets
- Optional panel failures (weapons, relics, stats, skills)
- Rendering failures for individual components

**Constructor:**
```python
ComponentBuildError(
    message: str,
    component_name: str = "UNKNOWN",
    original_error: Optional[Exception] = None,
    context: Optional[dict] = None
)
```

**Example:**
```python
try:
    weapon_panel = await build_weapon_panel(weapon_data)
except Exception as e:
    error = ComponentBuildError(
        message="Failed to render weapon panel",
        component_name="WeaponPanel",
        original_error=e
    )
    error.log()
    # Continue with card building
```

#### `AssetError`
**Severity:** WARNING
**Inherits from:** ComponentBuildError

Raised when asset loading or processing fails.

**Example:**
```python
try:
    img = await asset_manager.get_asset('char_portrait')
except Exception as e:
    raise AssetError(
        message="Failed to load character portrait",
        asset_name="char_portrait",
        original_error=e
    )
```

#### `DataFetchError`
**Severity:** WARNING
**Inherits from:** ComponentBuildError

Raised when external data fetch fails (API calls, network issues, etc.).

**Example:**
```python
try:
    showcase = await self.ef.get_showcase(uid)
except Exception as e:
    raise DataFetchError(
        message="Failed to fetch showcase data",
        data_source="Endfield API",
        uid=uid,
        original_error=e
    )
```

#### `RenderError`
**Severity:** WARNING
**Inherits from:** ComponentBuildError

Raised when image rendering or compositing fails.

**Example:**
```python
try:
    await asyncio.to_thread(composite_image, main_frame, (panel, location))
except Exception as e:
    raise RenderError(
        message="Failed to composite panel",
        component_name="WeaponPanel",
        original_error=e
    )
```

#### `ValidationError`
**Severity:** WARNING
**Inherits from:** ComponentBuildError

Raised when data validation fails.

**Example:**
```python
if not char_data:
    raise ValidationError(
        message="Character data is None",
        validation_type="CharacterData",
        context={"uid": uid}
    )
```

### ComponentBuildResult

A helper class for handling component build results with optional errors.

**Methods:**
- `ComponentBuildResult.ok(data, component_name)`: Create a successful result
- `ComponentBuildResult.fail(error, component_name)`: Create a failed result
- `unwrap_or(default)`: Get data or return default value
- `log_if_failed()`: Log error if this result is a failure

**Example:**
```python
result = await try_build_panel()
if not result:
    logger.warning(f"Panel build failed: {result.error}")
    panel = result.unwrap_or(None)
```

## Error Handling Patterns

### Pattern 1: Critical Component (Raise on Failure)

For components that are essential to card building (e.g., main frame):

```python
try:
    main_frame = await build_main_frame(char_data, user_img)
    if main_frame is None:
        raise CardBuildError(
            message="Main frame rendering failed",
            card_type="character",
            context={"component": "main_frame"}
        )
except CardBuildError:
    raise  # Re-raise critical errors
except Exception as e:
    error = CardBuildError(
        message=f"Failed to build main character frame: {e}",
        card_type="character",
        original_error=e
    )
    error.log()
    raise
```

### Pattern 2: Non-Critical Component (Log and Continue)

For optional components (weapons, relics, stats, skills):

```python
try:
    weapon_panel = await build_weapon_panel(weapon_data)
except Exception as e:
    error = ComponentBuildError(
        message=f"Failed to build weapon panel",
        component_name="WeaponPanel",
        original_error=e
    )
    error.log()
    # Continue without this panel
```

### Pattern 3: Async Component Gathering (Error Handling)

When building multiple components in parallel:

```python
results = await asyncio.gather(
    build_weapon_panel(weapon_data),
    build_relic_panel(equips),
    build_stats_panel(stats),
    build_skill_panel(skills),
    return_exceptions=True  # Important: return exceptions instead of raising
)

for component_name, result in zip(["weapon", "relic", "stats", "skill"], results):
    if isinstance(result, Exception):
        error = ComponentBuildError(
            message=f"Failed to build {component_name} panel",
            component_name=f"Panel[{component_name}]",
            original_error=result
        )
        error.log()
    elif result is not None:
        # Successfully built, use result
        composited_image = composite_panel(main_frame, result)
```

### Pattern 4: Data Fetch with Proper Error Wrapping

For external API calls:

```python
try:
    char_data = await self.ef.get_character_showcase(uid, char_index)
except Exception as e:
    error = DataFetchError(
        message="Failed to fetch character showcase",
        data_source="Endfield API",
        uid=uid,
        original_error=e,
        context={"char_index": char_index}
    )
    error.log()
    raise CardBuildError(
        message="Cannot build character card without character data",
        card_type="character",
        uid=uid,
        original_error=e
    )
```

## Logging Configuration

The package includes a `logging_config` module for centralized logging setup:

```python
from src.endfield_cards.logging_config import setup_logging
import logging

# Setup logging with file output
setup_logging(
    level=logging.INFO,
    log_file=Path("logs/endfield_cards.log"),
    debug=False
)
```

### Setup Options

- `level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `log_file`: Optional path to log file (enables file-based logging)
- `debug`: Enable debug mode with verbose output

### Features

- **Colored console output** on Unix-like systems for better readability
- **File logging** with rotation (10MB max, keeps 5 backups)
- **Consistent formatting** with timestamps
- **Suppressed third-party loggers** (PIL, urllib3, aiohttp)

## Usage in Client Code

```python
from src.endfield_cards import EFCard
from src.endfield_cards.logging_config import setup_logging
from src.endfield_cards.errors import CardBuildError
import logging

setup_logging(level=logging.INFO, debug=True)
logger = logging.getLogger(__name__)

async def main():
    async with EFCard() as efc:
        try:
            card = await efc.get_character_card(uid, char_index=2)
            logger.info("Character card built successfully")
        except CardBuildError as e:
            logger.error(f"Failed to build character card: {e}")
            # Handle gracefully
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
```

## Error Context

All error classes support context dictionaries for additional debugging information:

```python
error = CardBuildError(
    message="Failed to build character card",
    card_type="character",
    uid=4572346170,
    context={
        "char_index": 2,
        "template": 1,
        "asset_count": 5,
        "source": "Endfield API"
    }
)
```

This context is logged and helps in debugging:
```
[CARD_BUILD_FAILED] Failed to build character card | Context: {'card_type': 'character', 'uid': 4572346170, 'char_index': 2, ...}
```

## Best Practices

1. **Always provide context**: Include relevant debugging information in the `context` parameter
2. **Preserve original errors**: Pass the original exception to `original_error` parameter for stack trace preservation
3. **Use appropriate error types**: Choose the error class that best describes the failure
4. **Log before raising**: For component errors, log the error before continuing
5. **Differentiate critical from non-critical**: Only raise `CardBuildError` for failures that prevent card building
6. **Return exceptions from gather**: Use `return_exceptions=True` in `asyncio.gather()` for error handling
7. **Provide meaningful messages**: Error messages should clearly describe what failed and why

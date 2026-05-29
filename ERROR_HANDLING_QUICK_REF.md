# Error Handling Quick Reference

## Setup Logging

```python
from src.endfield_cards.logging_config import setup_logging
import logging

# One-time setup at application start
setup_logging(
    level=logging.INFO,
    log_file=None,  # Or Path("logs/endfield_cards.log")
    debug=True      # Enable for verbose output
)
```

## Error Handling in Client Code

```python
from src.endfield_cards import EFCard
from src.endfield_cards.errors import CardBuildError
import logging

logger = logging.getLogger(__name__)

async def build_cards(uid):
    async with EFCard() as efc:
        # Character card (raises on critical error)
        try:
            card = await efc.get_character_card(uid, char_index=2)
            logger.info("✓ Character card built")
        except CardBuildError as e:
            logger.error(f"✗ Character card failed: {e}")
            # Handle failure - card was not built
        
        # Profile card (same pattern)
        try:
            profile = await efc.get_profile_card(uid)
            logger.info("✓ Profile card built")
        except CardBuildError as e:
            logger.error(f"✗ Profile card failed: {e}")
        
        # Live stats (returns None on failure - no exception)
        stats = await efc.get_live_stats_card(uid, token)
        if stats:
            logger.info("✓ Stats card built")
        else:
            logger.warning("✗ Stats card failed (optional)")
```

## Creating Custom Components with Error Handling

### Critical Component (Raises on Failure)

```python
from ...errors import CardBuildError

async def build_critical_component(data):
    try:
        # Your component building logic
        result = await render_component(data)
        if result is None:
            raise CardBuildError(
                message="Component rendering returned None",
                card_type="character",
                context={"component": "critical"}
            )
        return result
    except CardBuildError:
        raise  # Re-raise critical errors
    except Exception as e:
        error = CardBuildError(
            message=f"Critical component failed: {e}",
            card_type="character",
            original_error=e
        )
        error.log()
        raise
```

### Non-Critical Component (Logs and Returns)

```python
from ...errors import ComponentBuildError

async def build_optional_component(data):
    try:
        # Your component building logic
        result = await render_component(data)
        return result
    except Exception as e:
        error = ComponentBuildError(
            message=f"Optional component failed: {e}",
            component_name="OptionalComponent",
            original_error=e
        )
        error.log()
        return None  # Return None to indicate failure
```

### Multiple Async Components

```python
import asyncio
from ...errors import ComponentBuildError

async def build_multiple_components(data):
    results = await asyncio.gather(
        build_component_a(data),
        build_component_b(data),
        build_component_c(data),
        return_exceptions=True  # IMPORTANT: Return exceptions instead of raising
    )
    
    panels = []
    for name, result in zip(["A", "B", "C"], results):
        if isinstance(result, Exception):
            # Component failed
            error = ComponentBuildError(
                message=f"Component {name} failed",
                component_name=f"Component[{name}]",
                original_error=result
            )
            error.log()
        elif result is not None:
            panels.append(result)
    
    return panels
```

## Error Types Summary

| Error | Severity | When to Use | Action |
|-------|----------|-------------|--------|
| `CardBuildError` | CRITICAL | Whole card can't be built | Raise immediately |
| `ComponentBuildError` | WARNING | Single component fails | Log and continue |
| `AssetError` | WARNING | Asset loading fails | Log and continue |
| `DataFetchError` | WARNING | API/data fetch fails | Log and consider retry |
| `RenderError` | WARNING | Image rendering fails | Log and continue |
| `ValidationError` | WARNING | Data validation fails | Log and use default |

## Common Patterns

### Pattern: Check Result with Default
```python
try:
    panel = await build_panel(data)
except ComponentBuildError as e:
    e.log()
    panel = None

if panel:
    # Use panel
else:
    # Use fallback
```

### Pattern: Wrap External Call
```python
from ...errors import DataFetchError, CardBuildError

try:
    data = await external_api.fetch(uid)
except Exception as e:
    error = DataFetchError(
        message="External API call failed",
        data_source="ExternalAPI",
        uid=uid,
        original_error=e
    )
    error.log()
    raise CardBuildError(
        message="Cannot build card without external data",
        card_type="character",
        uid=uid,
        original_error=e
    )
```

### Pattern: Component with Retry
```python
from ...errors import ComponentBuildError
import asyncio

async def build_with_retry(data, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await build_component(data)
        except Exception as e:
            if attempt == max_retries - 1:
                error = ComponentBuildError(
                    message=f"Component failed after {max_retries} attempts",
                    component_name="RetryableComponent",
                    original_error=e,
                    context={"attempts": max_retries}
                )
                error.log()
                return None
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

## Logging Best Practices

```python
import logging

logger = logging.getLogger(__name__)

# Info: Normal progress
logger.info(f"Building character card for uid={uid}")

# Warning: Non-critical issues
logger.warning(f"Asset not found, using fallback: {asset_name}")

# Error: Component failed but card continues
logger.error(f"Failed to render panel: {error}")

# Error: Card failed completely (use exception info)
logger.error(f"Card build failed: {error}", exc_info=True)

# Debug: Detailed information for troubleshooting
logger.debug(f"Processing character {char_id} with {num_relics} relics")
```

## Debugging

### View Full Error Context
```python
try:
    card = await efc.get_character_card(uid)
except CardBuildError as e:
    print(f"Error Code: {e.error_code}")
    print(f"Severity: {e.severity}")
    print(f"Message: {e.message}")
    print(f"Context: {e.context}")
    if e.original_error:
        print(f"Original: {e.original_error}")
```

### Enable Debug Logging
```python
from src.endfield_cards.logging_config import setup_logging
import logging

setup_logging(
    level=logging.DEBUG,
    debug=True
)
```

### Check Logs
```
[2026-01-20 10:30:45] src.endfield_cards.client | ERROR | Error building character card: Connection timeout
[2026-01-20 10:30:45] src.endfield_cards.character.template1.char1 | WARNING | Panel[weapon] failed with AssetError
[2026-01-20 10:30:46] src.endfield_cards.client | INFO | Character card built successfully (with degraded quality)
```

## Migration from Old Code

### Before (Errors Suppressed)
```python
try:
    card = await efc.get_character_card(uid)
except Exception as e:
    logger.error(f"Error: {e}")
    return Image.new("RGBA", ...)  # Silent failure
```

### After (Proper Error Handling)
```python
try:
    card = await efc.get_character_card(uid)
except CardBuildError as e:
    logger.error(f"Failed to build card: {e}")
    # Handle gracefully with user feedback
    return show_error_dialog(e)
```

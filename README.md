# Endfield Cards

[![PyPI version](https://img.shields.io/pypi/v/endfield-cards)](https://pypi.org/project/endfield-cards/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)

A powerful Python library for generating beautiful character and profile cards for **Endfield**. This library provides an easy-to-use interface to create stunning visual cards with character stats, weapons, relics, and profile information.

## Features

**Beautiful Card Templates** - Multiple professional templates for character showcase and profile cards

**Complete Character Information** - Display stats, skills, weapons, relics, and more

**Profile Cards** - Generate comprehensive profile cards with operator showcase

**Async Support** - Full async/await support for efficient operations

**Caching** - Smart asset caching for improved performance

**Easy Integration** - Simple API for quick integration into your projects

## Installation

### From PyPI (Recommended)

```bash
pip install endfield-cards
```

### From Source

```bash
git clone https://github.com/MR-LORD-REX/endfield-cards.git
cd endfield-cards
pip install -e .
```

## Dependencies

This library depends on:

- **[endfield-py](https://github.com/MR-LORD-REX/endfield)** - Core Endfield game data client
- **[enka.network](https://enka.network)** - Player data and asset provider


## Quick Start

### Basic Usage

```python
import asyncio
from ef_cards import EFCard

async def main():
    uid = 4225399080  # Your Endfield UID
    token = "your_token_here"  # Required for live stats and factory cards
    
    # Using async context manager (recommended)
    async with EFCard() as ef_card:
        # update assets on the first run or when new assets are available
        await ef_card.ef.update_assets()  
        await ef_card.update_builds()

        # Get a single character card
        char_card = await ef_card.get_character_card(uid, char_index=0)
        char_card.save("character_card.png")
        
        # Get all characters cards
        all_cards = await ef_card.get_all_characters_card(uid)
        
        # Get profile card with showcase
        profile = await ef_card.get_profile_card(uid)
        profile.card.save("profile_card.png")
        
        # Get live stats card (requires token)
        stats = await ef_card.get_live_stats_card(uid, token)
        if stats:
            stats.img.save("live_stats.png")
        
        # Get factory stats card (requires token)
        factory = await ef_card.get_factory_stats_card(uid, token)
        if factory:
            factory.save("factory_stats.png")

        char_card=await ef_card.get_character_build('endministrator')
        char_card[0].show()
        
        all=await ef_card.available_builds()
        print(all)

if __name__ == "__main__":
    asyncio.run(main())
```

### Without Context Manager

```python
import asyncio
from ef_cards import EFCard

async def main():
    ef_card = EFCard()
    try:
        char_card = await ef_card.get_character_card(4225399080, char_index=0)
        char_card.save("character_card.png")
    finally:
        await ef_card.close()  # Don't forget to close!

if __name__ == "__main__":
    asyncio.run(main())
```

## Available Methods

### Character Card

```python
# Get a single character card
card = await ef_card.get_character_card(
    uid: int,
    char_index: int = 0,
    user_img: Image.Image | None = None,
    template: int = 1
) -> Image.Image
```

### All Characters Cards

```python
# Get cards for all characters in a profile
cards = await ef_card.get_all_characters_card(
    uid: int,
    user_imgs: list[Image.Image] | None = None,
    template: int = 1
) -> list[Image.Image]
```

### Profile Card

```python
# Get a complete profile card with showcase
profile = await ef_card.get_profile_card(
    uid: int,
    template: int = 1
) -> ProfileCard_1
```

### Live Stats Card

```python
# Get live stats card (requires valid token)
stats = await ef_card.get_live_stats_card(
    uid: int,
    token: str,
    server: int = 3
) -> LiveStats | None
```

### Factory Stats Card

```python
# Get factory stats card with settlement details (requires valid token)
factory = await ef_card.get_factory_stats_card(
    uid: int,
    token: str,
    server: int = 3
) -> Image.Image | None
```

## Card Information

### Character Card Template 1 (1920x800)

Displays comprehensive character information including:

- **Main Frame** - Character artwork and basic stats
- **Weapon Panel** - Current weapon with stats
- **Relic Panel** - Equipped relics and bonuses
- **Skill Panel** - Character skills and cooldowns
- **Stats Panel** - Detailed character statistics

### Profile Card Template 1 (1080x1467)

Includes:

- **Player Profile** - UID, Authority Level, Exploration Level
- **Awakening Day** - Days since account creation
- **Operator Showcase** - 4 featured characters
- **Statistics** - Total operators, weapons, and files collected
- **Regional Development** - Development levels by region

### Live Stats Card (1024x355)

Real-time player statistics card (requires valid authentication token):

- **Sanity Points** - Current and maximum sanity
- **Recovery Timer** - Time until full sanity recovery
- **Daily Points** - Daily mission completion progress
- **Weekly Points** - Weekly mission score
- **Battle Pass** - Current battle pass level

### Factory Stats Card (1156x1755)

Comprehensive factory and settlement information card (requires valid authentication token):

- **Factory Overview** - Main factory level and money status
- **Settlement Details** - Per-settlement information including:
  - Settlement name and level
  - Assigned officer/character
  - Money storage status
- **Regional Breakdown** - Statistics for each region
- **Resource Management** - Visual progress bars for resources


## Example Output

### Character Card
![Character Card Example](https://github.com/MR-LORD-REX/endfield-cards/blob/main/src/examples/cards/char_card1.png)

### Profile Card
![Profile Card Example](https://github.com/MR-LORD-REX/endfield-cards/blob/main/src/examples/cards/profile_card1.png)

### Live stats card
![Stat card example](https://github.com/MR-LORD-REX/endfield-cards/blob/main/src/examples/cards/stats_card.png)

### Factory card
![Factory card example](https://github.com/MR-LORD-REX/endfield-cards/blob/main/src/examples/cards/factory_card.png)

### Character Guild Card
![Guild card example](https://github.com/MR-LORD-REX/endfield-builds/blob/main/output/endministrator.png)

## Data Sources

- **Game Data**: [endfield-py](https://github.com/MR-LORD-REX/endfield) - Endfield game data wrapper developed by me
- **Assets & Player Data**: [enka.network](https://enka.network) - Community-driven asset and player data provider
- **Guides data**: [prydwen.gg](https://www.prydwen.gg/) - For character build information and guides

## Configuration

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
async with EFCard(debug=True) as ef_card:
    # Your code here
    pass
```

### Custom Endfield Client

Use your own Endfield client instance:

```python
from endfield import Endfield

ef = Endfield()
async with EFCard(ef=ef) as ef_card:
    # Your code here
    pass
```
### How to get Token

- Check the [endfield-py documentation](https://github.com/MR-LORD-REX/endfield) for instructions on obtaining a valid token for accessing player data.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE.txt](LICENSE.txt) file for details.

## Disclaimer

This project is not affiliated with or endorsed by the developers of Endfield. All assets and game data are sourced from public APIs and are used for educational purposes only.

## Acknowledgments

- **endfield-py** - Library developed by me for accessing Endfield game data
- **endfield-builds** - Sister project for character build cards
- **enka.network** - For providing player data and asset caching

## Support

If you encounter any issues or have questions:

1. Check the [examples](src/examples/) directory for usage patterns
2. Enable debug mode to see detailed logs
3. Open an issue on [GitHub](https://github.com/MR-LORD-REX/endfield-cards/issues)
4. Contact me on [Telegram](https://t.me/The_Prime_Mover)

## Related Projects

- [endfield-py](https://github.com/MR-LORD-REX/endfield) - Core Endfield game data client
- [endfield-builds](https://github.com/MR-LORD-REX/endfield-builds) - Library for generating character build cards

---

**Note**: Make sure you have a valid Endfield UID to use this library. You can find your UID in-game .

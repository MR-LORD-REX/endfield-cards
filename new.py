from endfield import  Endfield
import asyncio

uid = 4225399080

async def main():
    async with Endfield(debug=True) as client:
        data = await client.get_showcase(uid)
        for char in data.characters:
            print(f"\n{'='*60}")
            print(f"Character: {char.name} ({char.str_id})")
            print(f"{'='*60}")
            if char.stats:
                print(f"STR: {char.stats.str_val}, AGI: {char.stats.agi}, WISD: {char.stats.wisd}, WILL: {char.stats.will}")
                print(f"HP: {char.stats.hp}, ATK: {char.stats.atk}, DEF: {char.stats.defense}")
                print(f"Crit Rate: {char.stats.crit_rate}%, Crit DMG: {char.stats.crit_dmg}%")
                print(f"Ultimate Gain: {char.stats.ultimate_gain_efficiency}%")
                print(f"Healing Received: {char.stats.healing_received_bonus}%")
                print(f"Arts Intensity: {char.stats.arts_intensity}")
        
asyncio.run(main())
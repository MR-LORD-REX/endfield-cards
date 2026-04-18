from endfield import  Endfield
import asyncio

uid = 4371235478

async def main():
    async with Endfield(debug=True) as client:
        data = await client.get_showcase(uid)
        json_data = data.model_dump_json(indent=2)
        with open("showcase.json", "w", encoding="utf-8") as fh:
            fh.write(json_data)
        for char in data.characters:
            print(f"\n{'='*60}")
            print(f"Character: {char.name} ({char.str_id})")
            print(f"{'='*60}")
            for stat in char.stats:
                print(stat)
            # for equip in char.equips:
            #     print(f"\n{'-'*40}")
            #     print(f"Equip: {equip.} ({equip.str_id})")

            
        
asyncio.run(main())
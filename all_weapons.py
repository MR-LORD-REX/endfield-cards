import aiohttp 
import json
import asyncio
import random

path="endfield/assets/suits.json"
base_url="https://endfieldtools.dev/localdb/optimized/equipment/suits/details/"

async def fetch_weapon_detail(session: aiohttp.ClientSession, weapon_id: int) -> dict:
    rand_time=random.uniform(0.1, 0.5)  
    await asyncio.sleep(rand_time)  
    async with session.get(f"{base_url}{weapon_id}.json") as response:
        print(f"Fetched weapon {weapon_id} with status {response.status}")
        print(f"calling {base_url}{weapon_id}.json")
        if response.status == 200:
            return await response.json()
        else:
            print(f"Failed to fetch weapon {weapon_id}: HTTP {response.status}")
            return {}

async def main():
    all_wep=json.load(open(path, encoding="utf-8"))
    tasks = []
    all_weapon_details = {}
    session=aiohttp.ClientSession()
    for item in all_wep.values():
        set_name = item["icon"].split("/")[-1].replace(".png", "").split("suit_")[-1]
        set_name = f"suit_{set_name}"
        tasks.append(fetch_weapon_detail(session,set_name ))
    weapon_details_list = await asyncio.gather(*tasks)
    for detail in weapon_details_list:
        all_weapon_details[detail.get("suitId", "unknown")] = {
            "setEffects": detail.get("setEffects", []),
        }
    with open("all_set_effect_details.json", "w", encoding="utf-8") as f:
        json.dump(all_weapon_details, f, indent=2, ensure_ascii=False)
        
    await session.close()
    
if __name__ == "__main__":
    asyncio.run(main())
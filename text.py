import asyncio, aiohttp, json

async def test():
    headers = {"Referer": "https://enka.network/", "Origin": "https://enka.network"}
    async with aiohttp.ClientSession(headers=headers) as sess:
        urls = [
            "https://api.enka.network/tooltip-data/ef/en/Weapons/wpn_sword_0006.json",
            "https://api.enka.network/tooltip-data/ef/en/Weapons/1797.json",
            "https://api.enka.network/tooltip-data/ef/en/medals.json",
        ]
        for url in urls:
            async with sess.get(url) as r:
                print(r.status, url)
                if r.status == 200:
                    d = await r.json(content_type=None)
                    print(json.dumps(d, indent=2, ensure_ascii=False)[:400])

asyncio.run(test())
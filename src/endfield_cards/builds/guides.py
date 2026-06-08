from pathlib import Path
from aiohttp import ClientSession
import json
from typing import Literal , List , Dict
import os

from .map import builds_map

assets_path = Path(__file__).parent.parent/"assets"/"builds"
file_path=assets_path/"builds_map.json"

map_file=Path(__file__).parent/"map.py"

if not file_path.exists():
    print("make sure to run client.update_builds() at least once to fetch the build data and create the builds_map.json file.")
    

def update_literal_mapping(data):
    # key as literal 
    py_file_text="from typing import Literal\n\n"
    py_file_text+="builds_map = Literal[\n"
    for key in data.keys():
        py_file_text+=f'    "{key}",\n'
    py_file_text+="]\n"
    with open(map_file, "w") as f:
        f.write(py_file_text)

async def fetch_build_data()->Dict[str,Dict[str,str]]:
    url="https://raw.githubusercontent.com/MR-LORD-REX/endfield-builds/main/ef_teams/assets/metadata/file_map.json"
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json(content_type=None)
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=2)
                update_literal_mapping(data)
                return data
            else:
                raise Exception(f"Failed to fetch build data: {response.status}")
            
def get_character_build(
    character:builds_map,
    )->str:
    if not file_path.exists():
        raise Exception("Build data not found. Please run update_builds() to fetch the latest build data.")
    with open(file_path, "r") as f:
        data = json.load(f)
    if character not in data:
        raise Exception(f"Build data for character '{character}' not found.")
    return data[character].get("raw_url", "")

def get_all_character_list(
    )->Dict[str,Dict[str,str]]:
    
    if not file_path.exists():
        raise Exception("Build data not found. Please run update_builds() to fetch the latest build data.")
    with open(file_path, "r") as f:
        data = json.load(f)
    all_c={}
    for char,info in data.items():
        all_c[char]={
            "icon_url":info.get("icon_url","")
        }
    return all_c


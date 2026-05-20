from pydantic import BaseModel, ConfigDict
from PIL import Image
from typing import List

class Character(BaseModel):
    name:str
    slot_index:int

class ProfileCard_1(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    card: Image.Image
    characters: List[Character]
    char_count: int
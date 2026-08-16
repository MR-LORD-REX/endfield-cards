from pydantic import BaseModel , ConfigDict
from PIL import Image

class DomainData(BaseModel):
    name: str
    slot: int

class MonumentShowcase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    card: Image.Image
    domains: list[DomainData]
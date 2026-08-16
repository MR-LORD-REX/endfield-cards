from pydantic import BaseModel, Field , ConfigDict
from PIL import Image
from endfield.models.auth.allc import AllCharacters

class AllChars(BaseModel):
    model_config=ConfigDict(arbitrary_types_allowed=True)
    
    card:Image.Image
    allChars:AllCharacters
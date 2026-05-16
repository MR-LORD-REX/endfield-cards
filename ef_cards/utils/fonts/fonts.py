from pathlib import Path
from typing import Optional , Literal
import os 
import logging

from PIL import ImageFont
from PIL import ImageDraw , Image

asset_base_path = Path(__file__).parent.parent.parent/"assets"
logger = logging.getLogger(__name__)

def get_font(font_name: Literal["EF_fonts"]="EF_fonts",size: int=20) -> Optional[ImageFont.FreeTypeFont]:
    font_path = asset_base_path / "fonts" / font_name
    font_file = str(font_path)+".ttf"
    if not os.path.exists(font_file):
        logger.error(f"Font '{font_name}' not found at path: {font_file}")
        return None
    try:
        font= ImageFont.truetype(font_file, size)
        return font
    except Exception as e:
        logger.error(f"Error loading font '{font_name}': {e}")
        return None
    
def put_text_in_center(text:str,font:ImageFont.FreeTypeFont,Draw:ImageDraw.ImageDraw,fill:tuple=(255,255,255)):
    bbox = Draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (Draw.im.size[0] - text_width) / 2
    y = (Draw.im.size[1] - text_height) / 2
    Draw.text((x, y), text, font=font, fill=fill)
    
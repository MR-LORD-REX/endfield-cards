from PIL import Image , ImageDraw, ImageFont
import asyncio


async def alpha_composite_center(base:Image.Image , overlay:Image.Image)-> None:
    base_w , base_h = base.size
    overlay_w , overlay_h = overlay.size
    pos_x = (base_w - overlay_w) // 2
    pos_y = (base_h - overlay_h) // 2
    base.alpha_composite(overlay,(pos_x,pos_y))
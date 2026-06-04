# Copyright (c) 2026 MR-LORD-REX
# All rights reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.


import logging
import asyncio
from PIL import Image

from endfield.models.basic.character import CharacterData
from .character import build_main_frame
from .weapon import build_weapon_panel
from .relics import build_relic_panel
from .skills import build_skill_panel
from .stats import build_stats_panel
from ...errors import ComponentBuildError, CardBuildError, RenderError

logger = logging.getLogger(__name__)

def composite_image(base:Image.Image,overlay:tuple[Image.Image,tuple[int,int]]):
    base.alpha_composite(overlay[0], overlay[1])


async def _build_character1(
    char_data: CharacterData,
    user_img: Image.Image | None = None
    ) -> Image.Image:
    """
    Build a character card from character data.
    Component failures (weapon, relics, stats, skills) are logged but don't stop the build.
    
    Args:
        char_data: Character data
        user_img: Optional user avatar image
        
    Returns:
        Image.Image: The character card image
    """
    try:
        main = char_data.main_attribute.attri_id
        sub = char_data.sub_attribute.attri_id
        
        try:
            main_frame = await build_main_frame(char_data, user_img)
            if main_frame is None:
                raise CardBuildError(
                    message="Main frame rendering failed",
                    card_type="character",
                    context={"component": "main_frame"}
                )
        except CardBuildError:
            raise
        except Exception as e:
            error = CardBuildError(
                message=f"Failed to build main character frame: {e}",
                card_type="character",
                original_error=e,
                context={"component": "main_frame"}
            )
            error.log()
            raise

        panels_data = [
            ("weapon", build_weapon_panel(weapon_data=char_data.weapon, main=main, sub=sub)),
            ("relic", build_relic_panel(char_data.equips)),
            ("stats", build_stats_panel(char_data.detailed_stats)),
            ("skill", build_skill_panel(char_data.skills, char_data.detailed_stats)),
        ]
        
        results = await asyncio.gather(
            *[panel_coro for _, panel_coro in panels_data],
            return_exceptions=True
        )

        compositing_tasks = []
        locations = [(1140, 50), (1328, 366), (19, 0), (19, 674)]
        panel_names = ["weapon", "relic", "stats", "skill"]
        
        for (name, _), location, result in zip(panels_data, locations, results):
            if isinstance(result, Exception):
                error = ComponentBuildError(
                    message=f"Failed to build {name} panel",
                    component_name=f"Panel[{name}]",
                    original_error=result
                )
                error.log()
            elif result is None:
                logger.warning(f"Panel[{name}] returned None, skipping compositing")
            else:
                try:
                    compositing_tasks.append(
                        asyncio.to_thread(composite_image, main_frame, (result, location))
                    )
                except Exception as e:
                    error = RenderError(
                        message=f"Failed to composite {name} panel",
                        component_name=f"Compositor[{name}]",
                        original_error=e
                    )
                    error.log()
        if compositing_tasks:
            try:
                await asyncio.gather(*compositing_tasks)
            except Exception as e:
                error = RenderError(
                    message=f"Failed during panel compositing",
                    component_name="CompositeRenderer",
                    original_error=e
                )
                error.log()
        return main_frame
        
    except CardBuildError:
        raise
    except Exception as e:
        error = CardBuildError(
            message=f"Unexpected error building character card: {e}",
            card_type="character",
            original_error=e
        )
        error.log()
        raise
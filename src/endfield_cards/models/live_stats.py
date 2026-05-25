from pydantic import BaseModel , ConfigDict
from PIL import Image
from datetime import datetime


class LiveStats(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    full_recovery_seconds: int
    full_recovery_minutes: int
    full_recovery_time: datetime | None
    img: Image.Image
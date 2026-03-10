# File Purpose: Hold Pydantic models (JSON structure)

from pydantic import BaseModel
from typing import Optional

# Function defining our EXIF data
class ExifData(BaseModel):
    camera_make: Optional[str] = None
    camera_model: Optional[str] = None
    iso: Optional[int] = None
    shutter_speed: Optional[str] = None
    aperture: Optional[float] = None

class ImageProcessResponse(BaseModel):
    status: str
    compressed_image_url: str
    exif: Optional[ExifData] = None
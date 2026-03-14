# File Purpose: Hold Pydantic models (JSON structure)

from pydantic import BaseModel
from typing import Optional, Dict, Any

# Function defining our EXIF data
class ExifData(BaseModel):
    camera_make: Optional[str] = None
    camera_model: Optional[str] = None
    iso: Optional[int] = None
    shutter_speed: Optional[str] = None
    aperture: Optional[float] = None

# response_model
class ImageProcessResponse(BaseModel):
    status: str
    compressed_image_url: str
    exif: Optional[Dict[str, Any]] = None
    compression_stats: Optional[Dict[str, Any]] = None 
    message: Optional[str] = None

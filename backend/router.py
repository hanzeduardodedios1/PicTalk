# Endpoints to handle JSON from APIs

from fastapi import APIRouter, UploadFile, File
from schemas import ImageProcessResponse
from services.image_service import extract_exif_data

router = APIRouter()
# Enter endpoints below

@router.post("/upload", response_model=ImageProcessResponse)
async def upload_image(file: UploadFile = File(...)):

    return {
        "status": "success",
        "exif": {
            "camera_make": "Sony",
            "iso": 100
        }
    }

@router.post("/extract", response_model=ImageProcessResponse)
async def extract_image_data(image_file: UploadFile = File(...)):

    # Pass uploaded file into image data extraction function
    dynamic_exif = extract_exif_data(image_file)

    return {
        "status": "success",
        "compressed_image_url": "Pending Cloudinary Integration", # Implement Cloudinary in later stage
        "exif": dynamic_exif
    }
# Endpoints to handle JSON from APIs

from fastapi import APIRouter, UploadFile, File, Depends
from schemas import ImageProcessResponse
from services.image_service import extract_exif_data, compress_image
from services.cloudinary_service import upload_to_cloudinary
from sqlalchemy.orm import Session
from database import SessionLocal
import crud


router = APIRouter()

# Creates a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
async def extract_image_data(image_file: UploadFile = File(...), db: Session = Depends(get_db)):


    # Get original size to compare
    image_file.file.seek(0,2) # Go to end of file
    original_size_kb = image_file.file.tell() / 1024

    # Extract exif data
    dynamic_exif = extract_exif_data(image_file)    

    # Compress the uploaded image
    compressed_bytes = compress_image(image_file)

    # Calculate the new size
    compressed_size_kb = len(compressed_bytes) / 1024 if compressed_bytes else 0

    # Upload to Cloudinary
    live_url = "Upload Failed"
    if compressed_bytes:
        live_url = upload_to_cloudinary(compressed_bytes)

    # Upload everything to database
    if live_url != "Upload Failed":
        crud.create_post(
            db=db,
            image_url=live_url,
            exif_data=dynamic_exif,
            original_size=original_size_kb,
            new_size=compressed_size_kb
        )
    
    return {
        "status": "success",
        "compressed_image_url": live_url, # Implement Cloudinary in later stage
        "exif": dynamic_exif,
        "compression_stats": {
            "original_size_kb": round(original_size_kb, 2),
            "new_size_kb": round(compressed_size_kb, 2),
            "saved_space": f"{round((1 - (compressed_size_kb / original_size_kb)) * 100 , 1)}%" if original_size_kb > 0 else "0%"
        },
        "message": "Image successfully processed and saved to database"
    }
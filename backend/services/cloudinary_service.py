# File Purpose: Use Cloudinary API

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os
import io

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_SECRET_API_KEY"),
    secure=True
)

def upload_to_cloudinary(image_bytes: bytes) -> str:
    try:
        byte_stream = io.BytesIO(image_bytes)
        response = cloudinary.uploader.upload(
            byte_stream,
            folder="pictalk_uploads",
            resource_type="image"
        )
        return response.get("secure_url")
    except Exception as e:
        print(f"Cloudinary Upload Error: {e}")
        return None
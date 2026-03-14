# File Purpose: Extract EXIF, resize, and convert to WebP

import io
import rawpy
from PIL import Image, ExifTags, ImageOps
from fastapi import UploadFile

def extract_exif_data(image_file: UploadFile) -> dict:
    extracted_data = {
        "camera_make": None,
        "camera_model": None,
        "iso": None,
        "shutter_speed": None,
        "aperture": None
    }
    try:
        # Re-read image_file by going to first index | Other functions do not reset the index
        image_file.file.seek(0)
        image = Image.open(image_file.file)
        raw_exif = image.getexif() if hasattr(image, 'getexif') else None
        if not raw_exif:
            return extracted_data
        
        # Decryption
        clean_exif = {}
        for tag_id, value in raw_exif.items():
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            clean_exif[tag_name] = value

        # Map data into our JSON
        if clean_exif.get("Make"):
            # Some cameras add null bytes \x00 at the end, strip them
            extracted_data["camera_make"] = str(clean_exif.get("Make")).strip(' \x00')
            
        if clean_exif.get("Model"):
            extracted_data["camera_model"] = str(clean_exif.get("Model")).strip(' \x00')
            
        exif_ifd = raw_exif.get_ifd(0x8769)
                
        if exif_ifd:
            # ISO (Tag ID: 34855)
            iso = exif_ifd.get(34855)
            if iso:
                extracted_data["iso"] = int(iso)
                        
            # Aperture (Tag ID: 33437)
            aperture = exif_ifd.get(33437)
            if aperture:
                extracted_data["aperture"] = round(float(aperture), 1)
                        
            # Shutter Speed (Tag ID: 33434)
            exposure = exif_ifd.get(33434)
            if exposure:
                try:
                    extracted_data["shutter_speed"] = f"{exposure.numerator}/{exposure.denominator}"
                except AttributeError:
                    extracted_data["shutter_speed"] = str(exposure)

    except Exception as e:
        print(f"Failed to extract EXIF: {e}")

    return extracted_data

def compress_image(image_file: UploadFile) -> bytes:
    try:
        # Re-read image_file by going to first index
        image_file.file.seek(0)
        # Change to lower_case
        filename = image_file.filename.lower()

        # Process large RAW files (cr2, nef, arw, dng)
        if filename.endswith(('.cr2', '.nef', '.arw', '.dng')):
            with rawpy.imread(image_file.file) as raw:
                rgb_array = raw.postprocess(use_camera_wb=True)
            img = Image.fromarray(rgb_array)
        # Processes normal images like .png or .jpg
        else: 
            img = Image.open(image_file.file)
            # ImageOps: for photos taken sideways on iPhone
            img = ImageOps.exif_transpose(img)

        # Standardize photo colors
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Maintain proper aspect ratio, implement a size cap (1920px) Standard HD
        max_size = (1920, 1920)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Save to memory as WEBP, a small resized file into RAM
        output_buffer = io.BytesIO()
        img.save(output_buffer, format="WEBP", quality=80)

        # Return the actual bytes
        return output_buffer.getvalue()
    except Exception as e:
        print(f"Compression Error: {e}")
        return None

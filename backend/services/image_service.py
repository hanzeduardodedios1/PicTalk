# File Purpose: Extract EXIF, resize, and convert to WebP

from PIL import Image, ExifTags
from fastapi import UploadFile

def extract_exif_data(image_file = UploadFile) -> dict:
    extracted_data = {
        "camera_make": None,
        "camera_model": None,
        "iso": None,
        "shutter_speed": None,
        "aperture": None
    }
    try:
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
            
        iso_val = clean_exif.get("ISOSpeedRatings") or clean_exif.get("ISO")
        if iso_val:
            extracted_data["iso"] = int(iso_val)

        # The data is a float, we clean it up appropriately
        f_number = clean_exif.get("FNumber")
        if f_number:
            extracted_data["aperture"] = round(float(f_number), 1)

        # Format to fraction rather than decimal
        exposure = clean_exif.get("ExposureTime")
        if exposure:
            try:
                extracted_data["shutter_speed"] = f"{exposure.numerator}/{exposure.denominator}"
            except AttributeError:
                # Fallback just in case a weird camera saves it as a standard string
                extracted_data["shutter_speed"] = str(exposure)

    except Exception as e:
        # If the file is corrupt or not an image, we print the error to the terminal
        # return empty dictionary to prevent server crash
        print(f"Failed to extract EXIF: {e}")

    return extracted_data

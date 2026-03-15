# Interactions with Database (CRUD: Create, Read, Operate, Delete)

from sqlalchemy.orm import Session
import models

def create_post(db: Session, image_url: str, exif_data: dict, original_size: float, new_size: float):
    db_post = models.Post(
        image_url=image_url,
        camera_make=exif_data.get("camera_make"),
        camera_model=exif_data.get("camera_model"),
        iso=exif_data.get("iso"),
        aperture=exif_data.get("aperture"),
        shutter_speed=exif_data.get("shutter_speed"),
        original_size_kb=original_size,
        new_size_kb=new_size
    )

    # Add to Database (similar to Git)
    db.add(db_post)
    # Commit changes to database
    db.commit()

    # Retrieves new database's ID
    db.refresh(db_post)

    return db_post


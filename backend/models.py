# Database models

from sqlalchemy import Column, Integer, String, Float
from database import Base

# DATABASE
class Post(Base):
    __tablename__ = "posts"

    # Database table ID
    id = Column(Integer, primary_key=True, index=True)

    # Cloudinary URL
    image_url = Column(String, nullable=False)

    # EXIF data
    camera_make = Column(String, nullable=True)
    camera_model = Column(String, nullable=True)
    iso = Column(Integer, nullable=True)
    shutter_speed = Column(String, nullable=True)
    aperture = Column(Float, nullable=True)

    # Compression stats (low prio)
    original_size_kb = Column(Float, nullable=True)
    new_size_kb = Column(Float, nullable=True)

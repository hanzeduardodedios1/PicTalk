from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from router import router
import models
from database import engine

# Create the database file including designed tables
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router)

# CORSMiddleware, enables backend to connect to browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


import os 
import json
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status, Security
from fastapi.security.api_key import APIKeyHeader
from sqlmodel import create_engine, SQLModel

#Static Data Json Loads
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/loads.json")
def read_static_db() -> List[dict]:
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def write_static_db(data: List[dict]):
    with open(DATA_PATH, "w") as f:
        json.dump(jsonable_encoder(data), f, indent=4)


#API Key Authentication
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    # Pull the expected key from Railway Environment Variables
    expected_key = os.getenv("INTERNAL_API_KEY")
    
    if api_key_header == expected_key:
        return api_key_header
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
    )


#Database setup 
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME")

# Construct the URL
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)

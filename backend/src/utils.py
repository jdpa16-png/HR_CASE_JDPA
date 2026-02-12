import os 
import json
from typing import List
from fastapi.encoders import jsonable_encoder


DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/loads.json")

def read_db() -> List[dict]:
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def write_db(data: List[dict]):
    with open(DATA_PATH, "w") as f:
        json.dump(jsonable_encoder(data), f, indent=4)

def get_api_key(api_key_header: str = Security(api_key_header)):
    # Pull the expected key from Railway Environment Variables
    expected_key = os.getenv("INTERNAL_API_KEY")
    
    if api_key_header == expected_key:
        return api_key_header
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
    )
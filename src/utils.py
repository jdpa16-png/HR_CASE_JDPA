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

import os
from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import json
from typing import List
from src.models import Load, MessageResponse   
from src.utils import read_db, write_db

app = FastAPI(title="Acme Logistics Inbound API", 
                  description="API for receiving inbound load data from carriers and forwarding to Acme's internal systems.",
                  version="0.1")

@app.get("/")
def health_check():
    """Health check endpoint to verify the service is running."""
    return {"status": "online", 
            "system": app.title, 
            "version": app.version}, 

@app.get("/loads", response_model=List[Load])
def get_all_loads():
    """Endpoint to retrieve all loads"""
    return read_db()

@app.get("/loads/{load_id}", response_model=Load) # Cambio a parámetro de ruta
def get_load(load_id: str):
    """Endpoint to retrieve a specific load information by load_id
    Args:        load_id (str): Unique identifier for the load
    Returns:       Load: The load data corresponding to the provided load_id
    """
    load = next((load for load in read_db() if load["load_id"] == load_id), None)
    if load is None:
        raise HTTPException(status_code=404, detail=f"Load with load_id {load_id} not found")
    return load

@app.post("/loads", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def add_load(new_load: Load):
    """Endpoint to include  a new load into our system
    Args:        new_load (Load): The load data to be added, validated against the Load model
    Returns:       str: Confirmation message with the load_id and total number of loads"""
    
    # Process the load data (e.g., save to database, forward to internal systems)
    # For this example, we'll just print it to the console
    print(f"Received load: {new_load}")

    # In a real implementation, you would save the load data to a database or forward it to another service here
    loads = read_db()

    if any(load['load_id'] == new_load.load_id for load in loads):
        raise HTTPException(
            status_code=400, 
            detail=f"The load ID {new_load.load_id} already exists in the system."
        )

    #jsonable_encoder is used to convert the Pydantic model to a JSON-serializable format
    new_load_data = jsonable_encoder(new_load)
    loads.append(new_load_data)
    write_db(loads)
    
    return MessageResponse(message=f"Load with load_id {new_load.load_id} received successfully. Total loads: {len(loads)}")    


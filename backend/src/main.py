import os
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import json
from typing import List
from src.models import Load, MessageResponse, CallLog
from src.utils import read_static_db, write_static_db, get_api_key, engine, init_db
from typing import Optional
from sqlmodel import Session



app = FastAPI(
    title="Acme Logistics Inbound API", 
    description="API for receiving inbound load data from carriers and forwarding to Acme's internal systems.",
    version="0.3",
    dependencies=[Depends(get_api_key)]
)

@app.middleware("http")
async def verify_happy_robot_request(request: Request, call_next):
    response = await call_next(request)
    return response

@app.on_event("startup")
def on_startup():
    init_db()

# Load Management Endpoints
@app.get("/")
def health_check():
    """Health check endpoint to verify the service is running."""
    return {"status": "online", 
            "system": app.title, 
            "version": app.version}, 

@app.get("/loads", response_model=List[Load], status_code=status.HTTP_200_OK) 
def get_loads(
    origin: Optional[str] = None, 
    destination: Optional[str] = None, 
    equipment_type: Optional[str] = None):

    """Endpoint to look for an specific load based on origin, destination, pickup date and equipment type
    
    Args:       
    
        origin (str): The starting location of the load
            
        destination (str): The ending location of the load
                
        equipment_type (str): The type of equipment required for the load (e.g., Dry Van, Reefer, Flatbed)
    
    Returns:       
    
        list[Load]: The list of loads data matching the search criteria, or a 404 error if no matching load is found
    """
    filtered_loads = read_static_db()

    # 2. Aplicamos filtros uno tras otro sobre el resultado anterior
    if origin:
        filtered_loads = [
            load for load in filtered_loads 
            if load["origin"].lower() == origin.lower()
        ]

    if destination:
        filtered_loads = [
            load for load in filtered_loads 
            if load["destination"].lower() == destination.lower()
        ]

    if equipment_type:
        filtered_loads = [
            load for load in filtered_loads 
            if load["equipment_type"].lower() == equipment_type.lower()
        ]
    
    if not filtered_loads:
        raise HTTPException(
            status_code=404, 
            detail="No matching loads found for the provided search criteria."
        )
    else:
        return filtered_loads

    if not loads:
        raise HTTPException(status_code=404, detail=f"No matching loads found for the provided search criteria.")
    return loads

@app.get("/loads/{load_id}", response_model=Load, status_code=status.HTTP_200_OK)
def get_load_by_id(load_id: str):
    """Endpoint to retrieve a specific load information by load_id

    Args:        
    
        load_id (str): Unique identifier for the load

    Returns:       
    
        Load: The load data corresponding to the provided load_id
    """
    load = next((load for load in read_static_db() if load["load_id"] == load_id), None)
    if load is None:
        raise HTTPException(status_code=404, detail=f"Load with load_id {load_id} not found")
    return load

@app.post("/loads", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def add_load(new_load: Load):
    """Endpoint to include  a new load into our system
    Args:        
    
        new_load (Load): The load data to be added, validated against the Load model

    Returns:       
    
        MessageResponse: Confirmation message with the load_id and total number of loads"""
    
    # Process the load data (e.g., save to database, forward to internal systems)
    # For this example, we'll just print it to the console
    print(f"Received load: {new_load}")

    # In a real implementation, you would save the load data to a database or forward it to another service here
    loads = read_static_db()

    if any(load['load_id'] == new_load.load_id for load in loads):
        raise HTTPException(
            status_code=400, 
            detail=f"The load ID {new_load.load_id} already exists in the system."
        )

    #jsonable_encoder is used to convert the Pydantic model to a JSON-serializable format
    new_load_data = jsonable_encoder(new_load)
    loads.append(new_load_data)
    write_static_db(loads)
    
    return MessageResponse(message=f"Load with load_id {new_load.load_id} received successfully. Total loads: {len(loads)}")    


#Call Log Endpoints 
@app.post("/log_call")
def log_call(data: CallLog):
    with Session(engine) as session:
        session.add(data)
        session.commit()
        session.refresh(data)
    return {"status": "saved", "id": data.Run_ID}

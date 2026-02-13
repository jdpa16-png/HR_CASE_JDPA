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

from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select

app = FastAPI(
    title="Acme Logistics Inbound API", 
    description="API for receiving inbound load data from carriers and forwarding to Acme's internal systems.",
    version="0.3",
    dependencies=[Depends(get_api_key)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def verify_api_key(request: Request):
    if request.method == "OPTIONS":
        return
    
    api_key = request.headers.get("x-api-key")
    if api_key != os.getenv("INTERNAL_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )

app.dependency_overrides = {} 
app.router.dependencies.append(Depends(verify_api_key))


@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def health_check():
    """
    Health check endpoint to verify the service is running.
    """
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

@app.post("/log_call_extraction")
def log_call(data: CallLog):
    """Endpoint to load a call extraction in our Database
    Args: data (CallLog): SQL Schema 

    Returns:  Status of insertion"""

    data.was_transferred = str(data.was_transferred).lower() == "true"
    data.flag_closed_deal = str(data.flag_closed_deal).lower() == "true"

    try:
        with Session(engine) as session:
            session.add(data)
            session.commit()
            session.refresh(data)
        return {"status": "success", "run_id": data.Run_ID}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/bulk_log_call_extraction", status_code=status.HTTP_201_CREATED)
def add_bulk_loads(new_loads: List[CallLog]): # Accept a List
    with Session(engine) as session:
        for load in new_loads:
            # Check for existing Run_ID to avoid primary key conflicts
            existing = session.get(CallLog, load.Run_ID)
            if not existing:
                session.add(load)
        
        session.commit()
        return {"message": f"Successfully processed {len(new_loads)} loads."}

@app.get("/all_call_extractions")
def get_all_call_extractions():
    """Fetch all call logs from the database for the dashboard."""
    with Session(engine) as session:
        statement = select(CallLog)
        results = session.exec(statement).all()
        return results

@app.get("/call_analytics")
def get_analytics():
    """ 
    Get Consolidated analysis of the stored calls
    """
    with Session(engine) as session:
        # 1. Fetch all logs for calculation
        statement = select(CallLog)
        logs = session.exec(statement).all()
        
        if not logs:
            return {"message": "No data available"}

        # --- Basic Stats ---
        total_calls = len(logs)
        closed_calls = [l for l in logs if l.flag_closed_deal]
        total_closed = len(closed_calls)
        
        # Success Rate
        success_rate = (total_closed / total_calls) * 100 if total_calls > 0 else 0
        
        # Financial Ratio: sum(final) / sum(initial)
        sum_final = sum(l.final_rate or 0 for l in logs)
        sum_initial = sum(l.original_rate or 0 for l in logs)
        rate_efficiency = (sum_final / sum_initial) * 100 if sum_initial > 0 else 0

        # --- Aggregations (Success by Origin) ---
        origin_stats = {}
        for l in logs:
            origin = l.Origin or "Unknown"
            if origin not in origin_stats:
                origin_stats[origin] = {"total": 0, "closed": 0}
            origin_stats[origin]["total"] += 1
            if l.flag_closed_deal:
                origin_stats[origin]["closed"] += 1

        # --- Sentiment & Tags ---
        sentiment_dist = {}
        tag_dist = {}
        for l in logs:
            # Sentiment
            s = l.carrier_sentiment or "Neutral"
            sentiment_dist[s] = sentiment_dist.get(s, 0) + 1
            # Call Tag
            t = l.call_tag or "Other"
            tag_dist[t] = tag_dist.get(t, 0) + 1

        # --- Evolution of Metrics (By Date) ---
        # Grouping success rate by day
        evolution = {}
        for l in logs:
            # Use the date part of your date_time
            date_key = l.date_time.date().isoformat() if l.date_time else "Unknown"
            if date_key not in evolution:
                evolution[date_key] = {"total": 0, "closed": 0}
            evolution[date_key]["total"] += 1
            if l.flag_closed_deal:
                evolution[date_key]["closed"] += 1

        return {
            "summary": {
                "total_calls": total_calls,
                "total_closed": total_closed,
                "success_rate": round(success_rate, 2),
                "rate_efficiency_ratio": round(rate_efficiency, 2),
                "avg_negotiation_turns": round(sum(l.turns or 0 for l in logs) / total_calls, 1)
            },
            "origin_success": origin_stats,
            "sentiment_distribution": sentiment_dist,
            "tag_distribution": tag_dist,
            "evolution": evolution
        }

    

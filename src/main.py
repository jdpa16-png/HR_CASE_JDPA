import os
from fastapi import FastAPI

app = FastAPI(title="Acme Logistics Inbound API", 
                  description="API for receiving inbound shipment data from carriers and forwarding to Acme's internal systems.",
                  version="0.1")

@app.get("/")
def health_check():
    """Health check endpoint to verify the service is running."""
    return {"status": "online", 
            "system": app.title, 
            "version": app.version}, 



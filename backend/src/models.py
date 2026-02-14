from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class Load(BaseModel):
    load_id: str =  Field(..., description="Unique identifier for the load")
    origin: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=100)
    pickup_datetime: datetime
    delivery_datetime: datetime
    equipment_type: str = Field(..., regex=r"^(Dry Van|Reefer|Flatbed)$", description="Equipment type must be one of: Dry Van, Reefer, Flatbed")
    loadboard_rate: float = Field(gt=0, description="rate must be greater than 0")
    notes: Optional[str] = None
    weight: int = Field(..., gt=0, description="weight must be greater than 0")
    commodity_type: str = Field(...,  description="Type of commodity being shipped")
    num_of_pieces: int = Field(..., ge=1, description="number of pieces must be greater than or equal to 1")
    miles: int = Field(..., gt=0, description="miles must be greater than 0")
    dimensions: str = Field(..., min_length=2)

    @field_validator('pickup_datetime', 'delivery_datetime')
    @classmethod
    def validate_datetimes(cls,v: datetime, info):
        if 'pickup_datetime' in info.data and v <= info.data['pickup_datetime']:
                raise ValueError('delivery_datetime must be after pickup_datetime')
        return v

class MessageResponse(BaseModel):
    message: str = Field(..., description="Response message confirming the action taken")

class CallLog(SQLModel, table=True):
    Run_ID: str = Field(primary_key=True)
    Carrier_Legal_Name: Optional[str] = None
    mc_number: Optional[str] = None
    Load_ID_Searched: Optional[int] = None
    Origin: Optional[str] = None
    destination: Optional[str] = None
    equipment_type: Optional[str] = None
    original_rate: Optional[float] = None
    final_rate: Optional[float] = None
    turns: Optional[int] = None
    
    flag_closed_deal: bool = Field(default=False)
    was_transferred:  bool = Field(default=False)
    
    call_tag: str
    carrier_sentiment: str
    transcript: Optional[str] = None

    date_time: datetime = Field(default_factory=datetime.utcnow)
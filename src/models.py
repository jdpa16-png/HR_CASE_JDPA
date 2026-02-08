from pydantic import BaseModel, Field
from typing import Optional


class Load(BaseModel):
    load_id: Field(..., description="Unique identifier for the load")
    origin: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=100)
    pickup_datetime: datetime
    delivery_datetime: datetime
    equipment_type: str = Field(..., pattern=r"^(Dry Van|Reefer|Flatbed)$", description="Equipment type must be one of: Dry Van, Reefer, Flatbed")
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
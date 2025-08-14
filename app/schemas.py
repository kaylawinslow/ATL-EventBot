from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
class EventOut(BaseModel):
    id: int
    source: Optional[str] = None
    source_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    venue_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    url: Optional[str] = None
    tags: Optional[str] = None
    class Config:
        from_attributes = True
class SuggestionParams(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    max_price: Optional[float] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    radius_km: Optional[float] = Field(default=20)
    q: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=50)
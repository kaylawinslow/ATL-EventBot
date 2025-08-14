from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from app.db import Base
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), index=True)
    source_id = Column(String(128), index=True, nullable=True)
    title = Column(String(300), index=True)
    description = Column(Text, nullable=True)
    category = Column(String(120), index=True, nullable=True)
    start_time = Column(DateTime, index=True, nullable=True)
    end_time = Column(DateTime, nullable=True)
    venue_name = Column(String(200), nullable=True)
    address = Column(String(300), nullable=True)
    city = Column(String(120), nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    price_min = Column(Float, nullable=True)
    price_max = Column(Float, nullable=True)
    url = Column(String(500), nullable=True)
    tags = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
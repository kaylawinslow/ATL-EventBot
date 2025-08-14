from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import List, Optional
from datetime import datetime
from app.db import SessionLocal
from app.models import Event
from app.schemas import EventOut
from app.recommender import score_event, haversine_km
app = FastAPI(title="ATL Plans Agent API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
@app.get("/health")
def health(): return {"status": "ok"}
@app.get("/events", response_model=List[EventOut])
def list_events(start_date: Optional[datetime]=Query(default=None), end_date: Optional[datetime]=Query(default=None),
                max_price: Optional[float]=Query(default=None, ge=0), lat: Optional[float]=Query(default=None),
                lon: Optional[float]=Query(default=None), radius_km: Optional[float]=Query(default=None, ge=0),
                q: Optional[str]=Query(default=None), db: Session=Depends(get_db)):
    stmt = select(Event); filters = []
    if start_date: filters.append(Event.start_time >= start_date)
    if end_date: filters.append(Event.start_time <= end_date)
    if max_price is not None: filters.append((Event.price_min == None) | (Event.price_min <= max_price))
    if q: like = f"%{q}%"; filters.append((Event.title.ilike(like)) | (Event.tags.ilike(like)))
    if filters: stmt = stmt.where(and_(*filters))
    events = db.execute(stmt).scalars().all()
    if lat is not None and lon is not None and radius_km is not None:
        filtered = []
        for ev in events:
            d = haversine_km(lat, lon, ev.lat, ev.lon) if (ev.lat and ev.lon) else None
            if d is None or d <= radius_km: filtered.append(ev)
        events = filtered
    return events
@app.get("/suggest", response_model=List[EventOut])
def suggest(start_date: Optional[datetime]=Query(default=None), end_date: Optional[datetime]=Query(default=None),
            max_price: Optional[float]=Query(default=None, ge=0), lat: Optional[float]=Query(default=None),
            lon: Optional[float]=Query(default=None), radius_km: Optional[float]=Query(default=20, ge=0),
            q: Optional[str]=Query(default=None), limit: int=Query(default=10, ge=1, le=50), db: Session=Depends(get_db)):
    events = db.execute(select(Event)).scalars().all()
    pre_filtered = []
    for ev in events:
        if start_date and ev.start_time and ev.start_time < start_date: continue
        if end_date and ev.start_time and ev.start_time > end_date: continue
        if lat is not None and lon is not None and radius_km is not None and ev.lat and ev.lon:
            d = haversine_km(lat, lon, ev.lat, ev.lon)
            if d is not None and d > radius_km: continue
        pre_filtered.append(ev)
    scored = [(score_event(ev, lat, lon, start_date, end_date, max_price, q)[0], ev) for ev in pre_filtered]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [ev for _, ev in scored[:limit]]
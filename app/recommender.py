from typing import Optional, Tuple
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime
from app.models import Event
def haversine_km(lat1, lon1, lat2, lon2) -> Optional[float]:
    try:
        if None in (lat1, lon1, lat2, lon2):
            return None
        R = 6371.0
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(1-a), sqrt(a))
        return R * c
    except Exception:
        return None
def score_event(ev: Event, user_lat: Optional[float], user_lon: Optional[float],
                start_date: Optional[datetime], end_date: Optional[datetime],
                max_price: Optional[float], query: Optional[str]) -> Tuple[float, Optional[float]]:
    score = 0.0; distance = None
    if start_date and ev.start_time and ev.start_time < start_date: score -= 5
    if end_date and ev.start_time and ev.start_time > end_date: score -= 5
    if user_lat is not None and user_lon is not None and ev.lat is not None and ev.lon is not None:
        distance = haversine_km(user_lat, user_lon, ev.lat, ev.lon)
        if distance is not None:
            score += 5 if distance <= 2 else 4 if distance <= 5 else 3 if distance <= 10 else 2 if distance <= 20 else 1
    if max_price is not None:
        price = ev.price_min if ev.price_min is not None else ev.price_max
        if price is not None: score += 3 if price <= max_price else -3
    hay = f"{(ev.title or '').lower()} {(ev.tags or '').lower()}"
    if query:
        if query.lower().strip() in hay: score += 4
    if ev.category: score += 0.5
    return score, distance
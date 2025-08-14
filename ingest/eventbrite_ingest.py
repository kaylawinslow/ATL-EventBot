import os, requests
from datetime import datetime
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Event
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("EVENTBRITE_TOKEN"); CITY = os.getenv("CITY", "Atlanta")
API_URL = "https://www.eventbriteapi.com/v3/events/search/"
def iso_parse(s):
    try: return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception: return None
def fetch_eventbrite(city: str, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": " ", "sort_by": "date", "location.address": city, "expand": "venue", "page": 1}
    items = []
    while True:
        resp = requests.get(API_URL, headers=headers, params=params, timeout=20); resp.raise_for_status()
        payload = resp.json(); events = payload.get("events", []); items.extend(events)
        pagination = payload.get("pagination", {})
        if not pagination.get("has_more_items"): break
        params["page"] = pagination.get("page_number", 1) + 1
        if len(items) >= 100: break
    return items
def upsert_events(events):
    db: Session = SessionLocal()
    try:
        inserted = 0
        for e in events:
            v = e.get("venue") or {}
            ev = Event(
                source="eventbrite",
                source_id=e.get("id"),
                title=(e.get("name") or {}).get("text") or "Untitled Event",
                description=(e.get("description") or {}).get("text"),
                category=None,
                start_time=iso_parse((e.get("start") or {}).get("utc")),
                end_time=iso_parse((e.get("end") or {}).get("utc")),
                venue_name=v.get("name"),
                address=(v.get("address") or {}).get("localized_address_display"),
                city=CITY,
                lat=float(v.get("latitude")) if v.get("latitude") else None,
                lon=float(v.get("longitude")) if v.get("longitude") else None,
                price_min=None, price_max=None, url=e.get("url"), tags=None,
            )
            db.add(ev); inserted += 1
        db.commit(); print(f"✅ Upserted {inserted} Eventbrite events.")
    finally:
        db.close()
if __name__ == "__main__":
    if not TOKEN:
        print("⚠️  EVENTBRITE_TOKEN not set — skipping API fetch and relying on seed data."); raise SystemExit(0)
    items = fetch_eventbrite(CITY, TOKEN); upsert_events(items)
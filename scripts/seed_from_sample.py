import json, os
from datetime import datetime
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Event
SEED_PATH = os.path.join("data", "seed_events.json")
def parse_dt(s):
    try: return datetime.fromisoformat(s)
    except Exception: return None
if __name__ == "__main__":
    if not os.path.exists(SEED_PATH): raise SystemExit(f"Seed file not found: {SEED_PATH}")
    with open(SEED_PATH, "r", encoding="utf-8") as f: data = json.load(f)
    db: Session = SessionLocal()
    try:
        inserted = 0
        for row in data:
            ev = Event(
                source=row.get("source", "seed"),
                source_id=row.get("source_id"),
                title=row.get("title", "Untitled Event"),
                description=row.get("description"),
                category=row.get("category"),
                start_time=parse_dt(row.get("start_time")),
                end_time=parse_dt(row.get("end_time")),
                venue_name=row.get("venue_name"),
                address=row.get("address"),
                city=row.get("city"),
                lat=row.get("lat"),
                lon=row.get("lon"),
                price_min=row.get("price_min"),
                price_max=row.get("price_max"),
                url=row.get("url"),
                tags=",".join(row.get("tags", [])) if isinstance(row.get("tags"), list) else row.get("tags"),
            )
            db.add(ev); inserted += 1
        db.commit(); print(f"✅ Inserted {inserted} events.")
    finally:
        db.close()
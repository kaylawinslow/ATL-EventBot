from app.models import Event
from app.recommender import score_event
from datetime import datetime
def test_score_prefers_nearby_free():
    ev = Event(title="Test Event", lat=33.78, lon=-84.39, price_min=0, price_max=0, start_time=datetime(2025,8,16,20,0))
    s, d = score_event(ev, 33.7819, -84.3883, datetime(2025,8,15), datetime(2025,8,20), 10, "test")
    assert s > 0
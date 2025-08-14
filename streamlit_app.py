import streamlit as st, requests, os
from datetime import datetime, timedelta
API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")
st.set_page_config(page_title="ATL Plans Agent", layout="wide")
st.title("ATL Plans Agent — Phase 1 (MVP)")
with st.sidebar:
    today = datetime.now().date()
    start_date = st.date_input("Start date", today)
    end_date = st.date_input("End date", today + timedelta(days=7))
    max_price = st.number_input("Max price ($)", min_value=0, value=25, step=1)
    lat = st.number_input("Your latitude", value=33.7819, format="%.6f")
    lon = st.number_input("Your longitude", value=-84.3883, format="%.6f")
    radius_km = st.slider("Radius (km)", 1, 50, 10)
    q = st.text_input("Search term", "")
    limit = st.slider("Suggestion count", 3, 20, 7)
params = {"start_date": f"{start_date}T00:00:00","end_date": f"{end_date}T23:59:59","max_price": max_price,
          "lat": lat,"lon": lon,"radius_km": radius_km,"q": q or None,"limit": limit}
col1, col2 = st.columns(2)
try:
    s = requests.get(f"{API_BASE}/suggest", params=params, timeout=20); s.raise_for_status(); suggestions = s.json()
except Exception as e:
    st.error(f"API error: {e}"); suggestions = []
with col1:
    st.subheader("Top Suggestions")
    if not suggestions: st.info("No suggestions yet or API not running.")
    for ev in suggestions:
        with st.container(border=True):
            st.markdown(f"### {ev['title']}")
            meta = [m for m in [ev.get('venue_name'), ev.get('city'), ev.get('start_time')] if m]
            st.write(" • ".join(map(str, meta)))
            if ev.get("description"):
                d = ev["description"]; st.write(d[:220] + ("…" if len(d)>220 else ""))
            price_text = "Free" if (ev.get("price_min") or 0)==0 else f"${ev.get('price_min','?')} - ${ev.get('price_max','?')}"
            st.write(f"**Price:** {price_text}")
            if ev.get("url"): st.link_button("Event link", ev["url"], use_container_width=True)
with col2:
    st.subheader("Map (suggestions)")
    pts = [{"lat": ev["lat"], "lon": ev["lon"]} for ev in suggestions if ev.get("lat") and ev.get("lon")]
    st.map(pts, size=10) if pts else st.info("No coordinates available.")
st.divider()
try:
    r = requests.get(f"{API_BASE}/events", params={k:v for k,v in params.items() if k!='limit'}, timeout=20); r.raise_for_status(); events = r.json()
    st.subheader("All Events (matching filters)"); st.write(f"Found {len(events)} events.")
    for ev in events: st.write(f"- {ev['title']} ({ev.get('venue_name','?')}, {ev.get('start_time','?')})")
except Exception as e:
    st.error(f"Could not load events. Error: {e}")
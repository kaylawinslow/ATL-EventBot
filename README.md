# ATL Plans Agent (Phase 1 MVP)

A beginner-friendly, Python-first project that recommends things to do in Atlanta based on time, budget, and neighborhood.
**Phase 1** delivers: clean data ingestion, a small database, a REST API, a simple UI, tests, and CI.

> **For hiring managers**: pragmatic, beginner-appropriate scope. See [`docs/FOR_EMPLOYERS.md`](docs/FOR_EMPLOYERS.md).

## Features
- Seed data (offline) + optional Eventbrite ingest
- SQLite via SQLAlchemy
- Rule-based recommender (distance/time/price/keyword)
- FastAPI (`/events`, `/suggest`) + docs at `/docs`
- Streamlit UI with filters + map
- Tests, Black/Flake8, GitHub Actions, Docker, Makefile

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
python scripts/init_db.py
python scripts/seed_from_sample.py
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs

In another terminal:
```bash
streamlit run streamlit_app.py
```

## Eventbrite (optional)
Copy `.env.example` to `.env`, set `EVENTBRITE_TOKEN`, then:
```bash
python ingest/eventbrite_ingest.py
```

## Tests & Lint
```bash
pytest -q
flake8 .
black --check .
```

## License
MIT

from app.db import engine, Base
from app.models import Event
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created.")
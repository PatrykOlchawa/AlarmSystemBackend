from sqlalchemy.orm import sessionmaker

from app.db.database import engine

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
def get_db():

    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()
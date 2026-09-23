from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/medicine_reminder_db"


engine = create_engine(
    DATABASE_URL,
    pool_size=10,         
    max_overflow=20,      
    pool_pre_ping=True   
)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    """
    Yields a unique database session per incoming API request, 
    and guarantees it closes securely when the operation completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from pastor.database import engine as database_engine
from collections.abc import Generator
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import sessionmaker, Session


__templates = Jinja2Templates(directory="pastor/templates")
def get_templates() -> Jinja2Templates:
    return __templates


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database_engine)
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        # TODO: add proper logging.
        print("[db error]: ", e)
    finally:
        db.close()

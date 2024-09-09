from pastor.config import DATABASE_DSN
from sqlalchemy import create_engine
from pastor.paste.models import Base


engine = create_engine(DATABASE_DSN, echo=True)


def init_db():
    Base.metadata.create_all(bind=engine)

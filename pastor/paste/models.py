from sqlalchemy import Text, Integer
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.orm import Mapped


class Base(DeclarativeBase):
    pass


class Paste(Base):
    __tablename__ = "pastes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    text: Mapped[str] = mapped_column(Text)

    def __repr__(self):
        return f"<Paste id={self.id} text={self.text[:20]}>"

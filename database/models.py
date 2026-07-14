from sqlalchemy import Column, Integer, String
from .bd import Base

class ItemDB(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"ItemDB(id={self.id},name='{self.name}')"
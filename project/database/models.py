from sqlalchemy import Column, Integer, String,Boolean
from .database import Base

class ItemDB(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"ItemDB(id={self.id},name='{self.name}')"

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String, unique=True,index=True,nullable=False)
    email = Column(String,unique=True,index=True,nullable=False)
    age = Column(Integer,nullable=True)
    hashed_password = Column(String,nullable=True)
    is_active = Column(Boolean,default=True)

    def __repr__(self):
        return f"UserDB(id={self.id},username='{self.username}',email='{self.email}')"
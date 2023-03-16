
from sqlalchemy import Column, Integer, String, Boolean
from src.database.database_base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String)
    is_active = Column(Boolean)
    
    def __init__(self, name, age, email, is_active):
        self.name = name
        self.age = age
        self.email = email
        self.is_active = is_active
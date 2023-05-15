from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import LargeBinary

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)

    wardrobe = relationship("Wardrobe", back_populates="user")

class Wardrobe(Base):
    __tablename__ = "wardrobe"

    id = Column(Integer, primary_key=True, index=True)

    item_image = Column(LargeBinary)
    item_name = Column(String(50), unique=True, index=True)
    item_category = Column(String(50), unique=True, index=True)
    item_tags = Column(String(150), unique=True, index=True)
    item_pref_weather = Column(String(50), unique=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="wardrobe")
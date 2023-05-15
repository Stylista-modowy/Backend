from typing import List, Optional

from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    username: str
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    
class WardrobeItemBase(BaseModel):
    item_name: str
    item_category: str
    item_tags: str
    item_pref_weather: str

class WardrobeItemCreate(WardrobeItemBase):
    item_image: bytes
    user_id: int

class WardrobeItem(WardrobeItemBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
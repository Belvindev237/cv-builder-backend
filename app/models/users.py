from pydantic import BaseModel ,EmailStr,Field
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
  username:str= Field(...,min_length=5,max_length=30)
  email:EmailStr
  password:str = Field(...,min_length=8)
  
class UserLogin(BaseModel):
  email:EmailStr
  password:str

class UserData(BaseModel):
  id:int
  username:str
  email:EmailStr
  created_at:datetime
   
class UserSave(UserRegister):
  hashed_password:str
  created_at:datetime=Field(default_factory=datetime.utcnow)
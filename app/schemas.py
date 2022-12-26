from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

# CreateUser class
class CreateUser(BaseModel):
    email:EmailStr
    password:str
    created_at:datetime = datetime.now()

# Get User class
class GetUser(BaseModel):
    id:int
    email: EmailStr
    created_at: datetime = datetime.now()

class UserLogin(BaseModel):
    email:EmailStr
    password:str

# Post class has the following columns with BaseModel checking the type and defaults
class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    created_at:datetime = datetime.now()

# For JWT token needed during authorization
class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str] = None

# Voting schema
# dir is the Direction of vote which is going to be either 0 or 1:
# 1 (like a post) or 0 (remove like of post) 
class Vote(BaseModel):
    post_id: int
    dir: Literal[0,1] # This allows only 0 and 1 as permitted values

    
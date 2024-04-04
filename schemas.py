from pydantic import BaseModel, EmailStr, validator
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'],
                           deprecated = 'auto')

# users Variaables
class user_creation(BaseModel):
    email : EmailStr
    password:str

    @validator('password')
    def Hash(cls,v):
        return pwd_context.hash(v)

class user_update(BaseModel):
    email : EmailStr
    password:str

    @validator('password')
    def Hash(cls,v):
        return pwd_context.hash(v)


# Posts Variaables
class create_post(BaseModel):
    Title:str
    content:str

class update_post(BaseModel):
    Title:str 
    content:str
    published:bool
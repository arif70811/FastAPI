from typing import Optional
from datetime import datetime
from pydantic import *


class create_post(BaseModel):
    Title:str
    content:str

class update_post(BaseModel):
    Title:str 
    content:str
    published:bool
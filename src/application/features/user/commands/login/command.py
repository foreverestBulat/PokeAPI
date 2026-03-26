from pydantic import BaseModel, EmailStr
from typing import List

class LoginCommand(BaseModel):
    email: EmailStr
    password: str

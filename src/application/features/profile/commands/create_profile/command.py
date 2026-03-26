from typing import Optional

from pydantic import BaseModel
from uuid import UUID


class CreateProfileCommand(BaseModel):
    name: str
    last_name: str
    description: str
    readme: str
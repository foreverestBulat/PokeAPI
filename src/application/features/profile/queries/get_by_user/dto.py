from pydantic import BaseModel, ConfigDict
from typing import Optional

class GetProfileByUserDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    last_name: str
    avatar: Optional[str] = None
    description: Optional[str] = None
    readme: Optional[str] = None

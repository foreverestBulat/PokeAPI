from typing import Optional

from pydantic import BaseModel


class UpdateProfileCommand(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    description: Optional[str] = None
    readme: Optional[str] = None
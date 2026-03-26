from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID


class UserListItemDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr    

    
    
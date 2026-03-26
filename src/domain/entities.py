from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class IEntity(ABC):
    id: Optional[UUID] = field(default=None, init=False)


@dataclass
class IBaseAuditableEntity(IEntity):
    created_date: datetime = field(default_factory=datetime.utcnow)
    updated_date: datetime = field(default_factory=datetime.utcnow)


@dataclass
class User(IBaseAuditableEntity):
    email: str = None
    hashed_password: str = None
    profile: "Profile" = None


@dataclass
class Profile(IBaseAuditableEntity):
    user: "User" = None
    name: str = None
    last_name: str = None
    avatar: str = None
    description: str = None
    readme: str = None

    
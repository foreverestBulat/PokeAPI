from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from domain.entities import User


@dataclass(frozen=True)
class TokenPayload:
    user_id: UUID
    email: str


class IJwtService(ABC):
    @abstractmethod
    def create_token(self, user: User) -> str: ...
    @abstractmethod
    def decode_token(self, token: str) -> Optional[TokenPayload]: ...


class IPasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str: ...
    @abstractmethod
    def verify(self, password: str, hashed_password: str) -> bool: ...



class IFileStorage(ABC):
    @abstractmethod
    async def upload(self, file_bytes: bytes, filename: str) -> str: ...

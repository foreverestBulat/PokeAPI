from dataclasses import dataclass
from domain.entities import User


@dataclass(frozen=True)
class UserCreatedEvent:
    user: User

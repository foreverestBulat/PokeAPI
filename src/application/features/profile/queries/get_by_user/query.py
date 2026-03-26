from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GetProfileByUserQuery:
    user_id: UUID

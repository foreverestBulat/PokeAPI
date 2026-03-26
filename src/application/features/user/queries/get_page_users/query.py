from dataclasses import dataclass


@dataclass(frozen=True)
class GetUsersPageQuery:
    page: int = 1
    size: int = 10

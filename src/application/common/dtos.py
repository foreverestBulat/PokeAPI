# src/domain/common/pagination.py
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar, List

T = TypeVar("T")

@dataclass(frozen=True)
class Result(Generic[T]):
    is_success: bool
    value: Optional[T] = None
    error: Optional[str] = None
    error_code: Optional[str] = None 

    @classmethod
    def ok(cls, value: T) -> "Result[T]":
        return cls(is_success=True, value=value)

    @classmethod
    def fail(cls, error: str, code: str = "ERROR") -> "Result[T]":
        return cls(is_success=False, error=error, error_code=code)

    @classmethod
    def success(cls) -> "Result[None]":
        return cls(is_success=True, value=None)


@dataclass(frozen=True)
class PagedResult(Result[List[T]]):
    total_count: int = 0
    page: int = 1
    size: int = 10

    @classmethod
    def ok_paged(cls, items: List[T], total: int, page: int, size: int) -> "PagedResult[T]":
        return cls(
            is_success=True,
            value=items,
            total_count=total,
            page=page,
            size=size
        )

    @property
    def total_pages(self) -> int:
        if self.size == 0: return 0
        return (self.total_count + self.size - 1) // self.size

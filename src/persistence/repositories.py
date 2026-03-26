from typing import Any, Dict, List, Optional, Type
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select, func

from application.common.dtos import PagedResult, Result
from application.interfaces.repositories import T, IGenericRepository, IProfileRepository, IUnitOfWork, IUserRepository
from domain.entities import Profile, User


class GenericRepository(IGenericRepository[T]):
    def __init__(self, session: AsyncSession, model_cls: Type[T]):
        self._session = session
        self._model_cls = model_cls
    
    async def get_by_id_async(self, id: UUID) -> Result[T]:
        entity = await self._session.get(self._model_cls, id)
        if not entity:
            return Result.fail(f"Entity {self._model_cls.__name__} not found")
        return Result.ok(entity)

    async def get_all_async(self) -> Result[List[T]]:
        result = await self._session.execute(select(self._model_cls))
        entities = result.scalars().all()
        return Result.ok(list(entities))

    async def get_page_async(self, page: int, size: int) -> PagedResult[T]:
        count_query = select(func.count()).select_from(self._model_cls)
        total = await self._session.scalar(count_query) or 0
        query = (
            select(self._model_cls)
            .offset((page - 1) * size)
            .limit(size)
        )
        result = await self._session.execute(query)
        items = result.scalars().all()
        return PagedResult.ok_paged(list(items), total, page, size)

    async def add_async(self, entity: T):
        self._session.add(entity)
        await self._session.flush() 
        return Result.ok(entity.id)

    async def update_async(self, entity: T) -> Result[None]:
        await self._session.merge(entity)
        return Result.success()

    async def delete_async(self, id) -> Result[None]:
        entity_result = await self.get_by_id_async(id)
        if not entity_result.is_success:
            return Result.fail("Entity not found for deletion")
        await self._session.delete(entity_result.value)
        return Result.success()


class UserRepository(GenericRepository[User], IUserRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
    
    async def find_by_email_async(self, email: str) -> Result[User]:
        query = select(User).filter_by(email=email)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            return Result.fail("User not found", "NOT_FOUND")
        return Result.ok(user)


class ProfileRepository(GenericRepository[Profile], IProfileRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Profile)

    async def get_by_user_async(self, user_id: UUID):
        query = select(Profile).where(User.id == user_id)
        result = await self._session.execute(query)
        profile = result.scalar_one_or_none()
        if not profile:
            return Result.fail("Profile not found", "NOT_FOUND")
        return Result.ok(profile)

class UnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        self._repositories: Dict[str, Any] = {}
        self._repo_mapping = {
            User: UserRepository,
            Profile: ProfileRepository,
        }
    
    async def __aenter__(self) -> "UnitOfWork":
        self._session = self._session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            await self.rollback_async()
        await self._session.close()
    
    def repository(self, entity_cls: Type[T]):
        name = entity_cls.__name__
        
        if name not in self._repositories:
            repo_class = self._repo_mapping.get(entity_cls, GenericRepository)
            if repo_class is GenericRepository:
                self._repositories[name] = GenericRepository(self._session, entity_cls)
            else:
                self._repositories[name] = repo_class(self._session)
                
        return self._repositories[name]
    
    async def save_async(self) -> int:
        try:
            await self._session.commit()
            return 1
        except Exception:
            await self.rollback_async()
            raise
    
    async def rollback_async(self) -> None:
        if self._session:
            await self._session.rollback()
from domain.entities import User
from application.common.dtos import Result
from application.features.user.queries.get_all_users.dto import UserListItemDto
from application.features.user.queries.get_all_users.query import GetUsersAllQuery
from application.interfaces.repositories import IUnitOfWork


class GetUsersAllQueryHandler:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def handle(self, query: GetUsersAllQuery) -> Result[list[UserListItemDto]]:
        async with self._uow as uow:
            repo = uow.repository(User)
            result = await repo.get_all_async()
            if not result.is_success:
                return Result.fail(result.error)
            dtos = [UserListItemDto.model_validate(user) for user in result.value]
            return Result.ok(dtos)

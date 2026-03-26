from domain.entities import User
from application.interfaces.repositories import IUnitOfWork
from application.common.dtos import Result
from application.features.user.queries.get_by_id.dto import GetUserByIdDto
from application.features.user.queries.get_by_id.query import GetUserByIdQuery

class GetUserByIdQueryHandler:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def handle(self, query: GetUserByIdQuery) -> Result[GetUserByIdDto]:
        async with self._uow as uow:
            user_repo = uow.repository(User)
            result = await user_repo.get_by_id_async(query.id)
            if not result.is_success:
                return Result.fail(result.error, "USER_NOT_FOUND")
            dto = GetUserByIdDto.model_validate(result.value)
            return Result.ok(dto)

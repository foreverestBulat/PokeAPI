from application.common.dtos import Result

from domain.entities import Profile
from application.interfaces.repositories import IUnitOfWork
from application.features.profile.queries.get_by_user.query import GetProfileByUserQuery
from application.features.profile.queries.get_by_user.dto import GetProfileByUserDto

class GetProfileByUserQueryHandler:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def handle(self, query: GetProfileByUserQuery) -> Result[GetProfileByUserDto]:
        async with self._uow as uow:
            profile_repo = uow.repository(Profile)
            result = await profile_repo.get_by_user_async(query.user_id)
            if not result.is_success:
                return Result.fail("Profile not found", "NOT_FOUND")
            dto = GetProfileByUserDto.model_validate(result.value)
            return Result.ok(dto)

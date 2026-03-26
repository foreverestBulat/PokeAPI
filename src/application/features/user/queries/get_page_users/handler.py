from domain.entities import User
from application.common.dtos import PagedResult
from application.features.user.queries.get_all_users.dto import UserListItemDto
from application.features.user.queries.get_page_users.query import GetUsersPageQuery
from application.interfaces.repositories import IUnitOfWork


class GetUsersPageQueryHandler:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def handle(self, query: GetUsersPageQuery) -> PagedResult[UserListItemDto]:
        async with self._uow as uow:
            repo = uow.repository(User)
            paged_result = await repo.get_page_async(query.page, query.size)
            if not paged_result.is_success:
                return PagedResult.fail(paged_result.error)
            dto_items = [UserListItemDto.model_validate(u) for u in paged_result.value]
            return PagedResult.ok_paged(
                items=dto_items,
                total=paged_result.total_count,
                page=paged_result.page,
                size=paged_result.size
            )

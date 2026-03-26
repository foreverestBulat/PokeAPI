from uuid import UUID

from application.common.dtos import Result
from application.features.profile.commands.create_profile.command import CreateProfileCommand
from application.interfaces.repositories import IUnitOfWork
from domain.entities import Profile, User


class CreateProfileCommandHandler:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def handle(self, command: CreateProfileCommand, user_id: UUID) -> Result[UUID]:
        async with self._uow as uow:
            profile_repo = uow.repository(Profile)
            existing = await profile_repo.get_by_user_async(user_id)
            if existing.is_success:
                return Result.fail("Profile already exists", "ALREADY_EXISTS")

            new_profile = Profile(
                user=(await uow.repository(User).get_by_id_async(user_id)).value,
                name=command.name,
                last_name=command.last_name
            )

            await profile_repo.add_async(new_profile)
            await uow.save_async()            
            return Result.ok(new_profile.id)

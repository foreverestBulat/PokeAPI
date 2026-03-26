# src/application/features/profiles/commands/update_profile/handler.py
from application.common.dtos import Result
from application.features.profile.commands.update_profile.command import UpdateProfileCommand
from application.interfaces.repositories import IUnitOfWork
from domain.entities import Profile


class UpdateProfileCommandHandler:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def handle(self, command: UpdateProfileCommand, user_id) -> Result[None]:
        async with self._uow as uow:
            profile_repo = uow.repository(Profile)
            result = await profile_repo.get_by_user_async(user_id)
            if not result.is_success:
                return Result.fail("Profile not found", "NOT_FOUND")

            profile = result.value

            if command.name is not None:
                profile.name = command.name
            if command.last_name is not None:
                profile.last_name = command.last_name
            if command.description is not None:
                profile.description = command.description
            if command.readme is not None:
                profile.readme = command.readme

            await profile_repo.update_async(profile)
            await uow.save_async()            
            return Result.success()

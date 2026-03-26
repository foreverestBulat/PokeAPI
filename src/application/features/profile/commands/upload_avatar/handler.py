from application.common.dtos import Result
from application.common.interfaces import IFileStorage
from application.features.profile.commands.upload_avatar.command import UploadAvatarCommand
from application.interfaces.repositories import IUnitOfWork
from domain.entities import Profile


class UploadAvatarCommandHandler:
    def __init__(self, uow: IUnitOfWork, storage: IFileStorage):
        self._uow = uow
        self._storage = storage

    async def handle(self, command: UploadAvatarCommand) -> Result[str]:
        async with self._uow as uow:
            profile_repo = uow.repository(Profile)
            result = await profile_repo.get_by_user_async(command.user_id)

            if not result.is_success:
                return Result.fail("Profile not found")

            file_url = await self._storage.upload(command.content, command.filename)
            profile = result.value
            profile.avatar = file_url

            await uow.save_async()
            
            return Result.ok(file_url)

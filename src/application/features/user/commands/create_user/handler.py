from uuid import UUID
from application.common.interfaces import IJwtService, IPasswordHasher
from application.features.user.commands.create_user.command import CreateUserCommand
from application.interfaces.repositories import IUnitOfWork
from domain.entities import User, Profile
from application.common.dtos import Result

class CreateUserCommandHandler:
    def __init__(self, uow: IUnitOfWork, hasher: IPasswordHasher):
        self._uow = uow
        self._hasher = hasher

    async def handle(self, command: CreateUserCommand) -> Result[UUID]:
        async with self._uow as uow:
            user_repo = uow.repository(User)
            existing = await user_repo.find_by_email_async(command.email)
            if existing.is_success:
                return Result.fail("User with this email already exists", "ALREADY_EXISTS")

            hashed_pw = self._hasher.hash(command.password)
            new_user = User(
                email=command.email,
                hashed_password=hashed_pw
            )

            await user_repo.add_async(new_user)
            await uow.save_async()
            return Result.ok(new_user.id)

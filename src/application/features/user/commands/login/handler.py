from application.common.dtos import Result
from application.common.interfaces import IJwtService, IPasswordHasher
from application.features.user.commands.login.command import LoginCommand
from application.interfaces.repositories import IUnitOfWork
from domain.entities import User


class LoginCommandHandler:
    def __init__(self, uow: IUnitOfWork, jwt_service: IJwtService, hasher: IPasswordHasher):
        self._uow = uow
        self._jwt_service = jwt_service
        self._hasher = hasher

    async def handle(self, command: LoginCommand) -> Result[str]:
        async with self._uow as uow:
            user_repo = uow.repository(User)
            user_result = await user_repo.find_by_email_async(command.email)
            
            if not user_result.is_success:
                return Result.fail("Invalid email or password", "AUTH_FAILED")

            user = user_result.value
            is_valid = self._hasher.verify(command.password, user.hashed_password)
            
            if not is_valid:
                return Result.fail("Invalid email or password", "AUTH_FAILED")

            token = self._jwt_service.create_token(user)            
            return Result.ok(token)



# from fastapi import Depends
# from application.interfaces.repositories import IUnitOfWork
# from application.common.interfaces.identity import IJwtService
# from application.common.interfaces.password import IPasswordHasher

# # Импорт реализаций (Infrastructure/Persistence)
# from persistence.database import async_session_factory
# from persistence.unit_of_work import UnitOfWork
# from infrastructure.identity.jwt_service import JwtService
# from infrastructure.security.password_hasher import PasswordHasher

# # Импорт хендлеров
# from application.features.users.commands.create_user.handler import CreateUserCommandHandler
# from application.features.users.commands.login.handler import LoginCommandHandler
# from application.features.users.queries.get_user_by_id.handler import GetUserByIdQueryHandler
# from application.features.profiles.queries.get_profile_by_user.handler import GetProfileByUserQueryHandler
# from application.features.profiles.commands.update_profile.handler import UpdateProfileCommandHandler

# 1. Базовые инфраструктурные зависимости
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from application.common.interfaces import IFileStorage, IJwtService, IPasswordHasher
from application.features.profile.commands.create_profile.handler import CreateProfileCommandHandler
from application.features.profile.commands.update_profile.handler import UpdateProfileCommandHandler
from application.features.profile.commands.upload_avatar.handler import UploadAvatarCommandHandler
from application.features.profile.queries.get_by_user.handler import GetProfileByUserQueryHandler
from application.features.user.commands.create_user.handler import CreateUserCommandHandler
from application.features.user.commands.login.handler import LoginCommandHandler
from application.features.user.queries.get_all_users.handler import GetUsersAllQueryHandler
from application.features.user.queries.get_by_id.handler import GetUserByIdQueryHandler
from application.features.user.queries.get_page_users.handler import GetUsersPageQueryHandler
from application.interfaces.repositories import IUnitOfWork
from config import get_secret_key
from domain.entities import User
from infrustructure.services import JwtService, LocalFileStorage, PasswordHasher
from persistence.repositories import UnitOfWork
from persistence.database import async_session_factory


def get_uow() -> IUnitOfWork:
    return UnitOfWork(async_session_factory)

def get_jwt_service() -> IJwtService:
    return JwtService(secret=get_secret_key())

def get_password_hasher() -> IPasswordHasher:
    return PasswordHasher()

def get_storage() -> IFileStorage:
    return LocalFileStorage()

def get_create_user_handler(
    uow: IUnitOfWork = Depends(get_uow),
    hasher: IPasswordHasher = Depends(get_password_hasher)
) -> CreateUserCommandHandler:
    return CreateUserCommandHandler(uow, hasher)

def get_login_handler(
    uow: IUnitOfWork = Depends(get_uow),
    jwt_service: IJwtService = Depends(get_jwt_service),
    hasher: IPasswordHasher = Depends(get_password_hasher)
) -> LoginCommandHandler:
    return LoginCommandHandler(uow, jwt_service, hasher)

def get_create_profile_handler(
    uow: IUnitOfWork = Depends(get_uow),
    hasher: IPasswordHasher = Depends(get_password_hasher)
) -> CreateProfileCommandHandler:
    return CreateProfileCommandHandler(uow)

def get_update_profile_handler(
    uow: IUnitOfWork = Depends(get_uow)
) -> UpdateProfileCommandHandler:
    return UpdateProfileCommandHandler(uow)

def get_user_by_id_handler(
    uow: IUnitOfWork = Depends(get_uow)
) -> GetUserByIdQueryHandler:
    return GetUserByIdQueryHandler(uow)

def get_profile_by_user_handler(
    uow: IUnitOfWork = Depends(get_uow)
) -> GetProfileByUserQueryHandler:
    return GetProfileByUserQueryHandler(uow)

def get_users_all_handler(
    uow: IUnitOfWork = Depends(get_uow)
) -> GetUsersAllQueryHandler:
    return GetUsersAllQueryHandler(uow)

def get_users_page_handler(
    uow: IUnitOfWork = Depends(get_uow)
) -> GetUsersPageQueryHandler:
    return GetUsersPageQueryHandler(uow)

def get_upload_avatar_handler(
    uow: IUnitOfWork = Depends(get_uow),
    storage: IFileStorage = Depends(get_storage)
) -> UploadAvatarCommandHandler:
    return UploadAvatarCommandHandler(uow, storage)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    jwt_service: IJwtService = Depends(get_jwt_service),
    uow: IUnitOfWork = Depends(get_uow)
) -> User:
    payload = jwt_service.decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    async with uow:
        user_repo = uow.repository(User)
        result = await user_repo.get_by_id_async(payload.user_id)
        
        if not result.is_success:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="User not found"
            )
        
        return result.value


async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
    jwt_service: IJwtService = Depends(get_jwt_service)
) -> UUID:
    payload = jwt_service.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload.user_id
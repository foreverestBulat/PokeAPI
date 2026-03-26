from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File

from application.common.dtos import Result
from application.features.profile.commands.create_profile.command import CreateProfileCommand
from application.features.profile.commands.create_profile.handler import CreateProfileCommandHandler
from application.features.profile.commands.update_profile.command import UpdateProfileCommand
from application.features.profile.commands.update_profile.handler import UpdateProfileCommandHandler
from application.features.profile.commands.upload_avatar.command import UploadAvatarCommand
from application.features.profile.commands.upload_avatar.handler import UploadAvatarCommandHandler
from application.features.profile.queries.get_by_user.dto import GetProfileByUserDto
from application.features.profile.queries.get_by_user.handler import GetProfileByUserQueryHandler
from application.features.profile.queries.get_by_user.query import GetProfileByUserQuery
from dependencies import get_create_profile_handler, get_current_user_id, get_profile_by_user_handler, get_update_profile_handler, get_upload_avatar_handler

profile_router = APIRouter(prefix="/profile", tags=["profile"])

@profile_router.get("/me")
async def get_my_profile(
    user_id: UUID = Depends(get_current_user_id),
    handler: GetProfileByUserQueryHandler = Depends(get_profile_by_user_handler)
) -> Result[GetProfileByUserDto]:
    return await handler.handle(GetProfileByUserQuery(user_id))


@profile_router.post("/me")
async def add_my_profile(
    command: CreateProfileCommand,
    user_id: UUID = Depends(get_current_user_id),
    handler: CreateProfileCommandHandler = Depends(get_create_profile_handler)
) -> Result[UUID]:
    return await handler.handle(command, user_id)


@profile_router.put("/me")
async def update_profile(
    command: UpdateProfileCommand,
    user_id: UUID = Depends(get_current_user_id),
    handler: UpdateProfileCommandHandler = Depends(get_update_profile_handler)
) -> Result[None]:
    return await handler.handle(command, user_id)


@profile_router.post("/me/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    user_id: UUID = Depends(get_current_user_id),
    handler: UploadAvatarCommandHandler = Depends(get_upload_avatar_handler)
) -> Result[str]:
    content = await file.read()
    command = UploadAvatarCommand(user_id=user_id, content=content, filename=file.filename)
    return await handler.handle(command)


@profile_router.get("/other")
async def get_profile(
    user_id: UUID,
    handler: GetProfileByUserQueryHandler = Depends(get_profile_by_user_handler)
) -> Result[GetProfileByUserDto]:
    return await handler.handle(GetProfileByUserQuery(user_id))

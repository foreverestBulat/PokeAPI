from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from application.common.dtos import Result
from application.features.user.commands.create_user.command import CreateUserCommand
from application.features.user.commands.create_user.handler import CreateUserCommandHandler
from application.features.user.commands.login.command import LoginCommand
from application.features.user.commands.login.handler import LoginCommandHandler
from application.features.user.queries.get_all_users.dto import UserListItemDto
from application.features.user.queries.get_all_users.handler import GetUsersAllQueryHandler
from application.features.user.queries.get_all_users.query import GetUsersAllQuery
from application.features.user.queries.get_by_id.dto import GetUserByIdDto
from application.features.user.queries.get_by_id.handler import GetUserByIdQueryHandler
from application.features.user.queries.get_by_id.query import GetUserByIdQuery
from application.features.user.queries.get_page_users.handler import GetUsersPageQueryHandler
from application.features.user.queries.get_page_users.query import GetUsersPageQuery
from dependencies import get_create_user_handler, get_current_user_id, get_login_handler, get_user_by_id_handler, get_users_all_handler, get_users_page_handler


user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.post("/register")
async def register(
    command: CreateUserCommand,
    handler: CreateUserCommandHandler = Depends(get_create_user_handler)
) -> Result[UUID]:
    return await handler.handle(command)
    

@user_router.post("/login")
async def login(
    command: LoginCommand,
    handler: LoginCommandHandler = Depends(get_login_handler)
) -> Result[str]:
    return await handler.handle(command)
    

@user_router.get("/me")
async def get_me(
    current_user_id: UUID = Depends(get_current_user_id),
    handler: GetUserByIdQueryHandler = Depends(get_user_by_id_handler)
) -> Result[GetUserByIdDto]:
    return await handler.handle(GetUserByIdQuery(current_user_id))


@user_router.get("/other")
async def get(
    user_id: UUID,
    handler: GetUserByIdQueryHandler = Depends(get_user_by_id_handler)
):
    return await handler.handle(GetUserByIdQuery(user_id))


@user_router.get("/all")
async def get_all(
    handler: GetUsersAllQueryHandler = Depends(get_users_all_handler)
) -> Result[List[UserListItemDto]]:
    return await handler.handle(GetUsersAllQuery())


@user_router.get("/page")
async def get_page(
    page: int,
    size: int,
    handler: GetUsersPageQueryHandler = Depends(get_users_page_handler) 
):
    return await handler.handle(GetUsersPageQuery(page, size))
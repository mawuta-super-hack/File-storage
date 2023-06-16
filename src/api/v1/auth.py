from fastapi import APIRouter

from schemas.db_schemas import UserCreate, UserRead
from services.users import auth_backend, fastapi_users

api_auth_router = APIRouter()


api_auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

api_auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

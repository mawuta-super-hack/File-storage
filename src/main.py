import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import auth, base
from core.config import app_settings
from schemas.db_schemas import UserCreate, UserRead
from services.users import auth_backend, fastapi_users

app = FastAPI(
    title=app_settings.app_title,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse
)



app.include_router(auth.api_auth_router)

app.include_router(base.router, prefix='/api/v1', tags=['files'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_settings.host,
        port=app_settings.port
    )
# uvicorn main:app --host 127.0.0.1 --port 8080 --reload

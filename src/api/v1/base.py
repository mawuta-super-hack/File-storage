import os
import sys
import uuid
from pathlib import Path
from typing import Annotated, Any, Optional

import aiofiles
from fastapi import (APIRouter, Depends, HTTPException, Request, UploadFile,
                     status)
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from db.db import User, get_session
from schemas.db_schemas import FileRead, FileReadList
from services.files import file_crud
from services.users import current_active_user

# from schemas.urls import (HistoryList, URLCreate, URLCreateList, URLDelete,
#                          URLRead, URLReadList)
# from services.urls import url_crud

router = APIRouter()
FILE_FOLDER: str = 'files'
MEDIA_URL = '/media/'

#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

@router.get(
    '/ping',
    summary='Get services status',
    description='Execute a database, cache etc ping.')
async def read_status(db: AsyncSession = Depends(get_session)) -> dict:
    db_response_time = await file_crud.ping_db(db)
    return {
        'api': 'v1',
        'python': sys.version_info,
        'db': db_response_time
    }


@router.get(
    '/files',
    # status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_model= list[FileReadList],
    summary='Get files',
    description='Return information about uploaded files.')
async def read_files(
    *,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_active_user)
    # short_url_id: str
) -> Any:
    db_obj = await file_crud.get_multi(db=db)
    return db_obj


@router.post(
    '/files/upload',
    response_model=FileRead,
    summary='Upload a file',
    description='Upload a file in storage.')
async def upload(
    *, db: AsyncSession = Depends(get_session),
    user: User = Depends(current_active_user),
    file: UploadFile, 
    path: str
    # short_url_id: str,
) -> Any:
    id = uuid.uuid4()
    filename = file.filename
    out_file_path = rf'{FILE_FOLDER}/{id}'
    file_path = rf'{path}/{filename}'
    size = 0

    #user_folder = os.path.join(FILE_FOLDER, filename)
    #if path:
    #    user_folder = os.path.join(user_folder, path)
    #folder = Path(user_folder)
    #if not Path.exists(folder):
    #    Path(folder).mkdir(parents=True, exist_ok=True)
    #    file_size = 0
    #async with aiofiles.open(Path(folder), 'wb') as f:

    async with aiofiles.open(out_file_path, 'wb') as f:
        while content := await file.read(2 ** 16):
            size += len(content)  # async read chunk
            await f.write(content)  # async write chunk

    obj_in = {
        'id': id,
        'path': file_path,
        'name': filename,
        'size': size,
        'author': user.id
        #created_by=user.id,
        #is_downloadable=True
    }
    db_obj = await file_crud.create(db=db, obj_in=obj_in)
    return db_obj


@router.get(
    '/files/download',
    status_code=status.HTTP_200_OK,
    
    summary='Download a file',
    description='Download a file with path parameters: path and id.')
async def delete_url(
    *,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_active_user),
    path: Optional[str] = None,
    file_id: Optional[str] = None,
    # short_url_id: str
) -> Any:
    file = await file_crud.get(db=db, id=file_id, path=path)
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found."
        )
    return FileResponse(
        rf'{FILE_FOLDER}/{file.id}',
        media_type='application/octet-stream',
        filename=file.name
    )

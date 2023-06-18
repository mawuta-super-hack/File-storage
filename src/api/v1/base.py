import sys
import uuid
from typing import Any

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from core.logger import my_logger as logger
from db.db import User, get_session
from schemas.db_schemas import FileRead, FileReadList
from services.files import file_crud
from services.users import current_active_user

router = APIRouter()
FILE_FOLDER: str = 'files'


@router.get(
    '/ping',
    summary='Get services status',
    description='Execute a database, cache etc ping.')
async def read_status(db: AsyncSession = Depends(get_session)) -> dict:
    logger.info('Get status.')
    db_response_time = await file_crud.ping_db(db)
    return {
        'api': 'v1',
        'python': sys.version_info,
        'db': db_response_time
    }


@router.get(
    '/files',
    response_model=list[FileReadList],
    summary='Get files',
    description='Return information about uploaded files.')
async def read_files(
    *,
    db: AsyncSession = Depends(get_session),
    user: User = Depends(current_active_user),
    max_result: int | None = None,
    offset: int | None = None
) -> Any:
    logger.info('Get all files.')
    db_obj = await file_crud.get_multi(
        db=db, max_result=max_result, offset=offset)
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
) -> Any:
    logger.info('Start create a file object.')
    id = uuid.uuid4()
    filename = file.filename
    out_file_path = rf'{FILE_FOLDER}/{id}'
    file_path = rf'{path}/{filename}'
    size = 0
    logger.info('Start upload a file.')
    async with aiofiles.open(out_file_path, 'wb') as f:
        while content := await file.read(2 ** 16):
            size += len(content)
            await f.write(content)

    obj_in = {
        'id': id,
        'path': file_path,
        'name': filename,
        'size': size,
        'author': user.id
    }
    logger.info('Start create file in db.')
    db_obj = await file_crud.create(db=db, obj_in=obj_in)
    logger.info('Return upload file.')
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
    path: str | None = None,
    file_id: str | None = None
) -> Any:
    logger.info('Get file object in db.')
    file = await file_crud.get(db=db, id=file_id, path=path)
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found."
        )
    logger.info('Return file.')
    return FileResponse(
        rf'{FILE_FOLDER}/{file.id}',
        media_type='application/octet-stream',
        filename=file.name
    )

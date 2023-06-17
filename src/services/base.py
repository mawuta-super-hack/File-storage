import datetime
from typing import Generic, Optional, Type, TypeVar

import asyncpg
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from core.logger import my_logger as logger
from db.db import Base
from models.db_models import FileModel

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class Repository:
    """Basic crud class."""

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDBFiles(Repository, Generic[ModelType, CreateSchemaType]):
    """CRUD class for File model."""

    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get_multi(
            self,
            db: AsyncSession,
    ) -> Optional[ModelType]:
        """Get all files."""
        statement = select(self._model)
        results = await db.execute(statement=statement)
        return results.scalars().all()

    async def create(
            self,
            db: AsyncSession,
            *,
            obj_in: CreateSchemaType
    ) -> ModelType:
        """Upload a file."""
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = FileModel(**obj_in_data)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
        except ValueError as err:
            logger.exception(
                f'File is not upload. Error - {err}')
        return db_obj

    async def get(
            self,
            db: AsyncSession,
            path: str,
            id: str
    ) -> ModelType:
        """Download a file."""
        try:
            if id:
                statement = select(self._model).where(self._model.id == id)
            else:
                statement = select(self._model).where(self._model.path == path)
            results = await db.execute(statement=statement)
        except ValueError as err:
            logger.exception(
                f'File is not found. Error - {err}')
        return results.scalar_one_or_none()

    async def ping_db(self, db: AsyncSession):
        """Return ping db time."""
        statement = text('SELECT version();')
        start = datetime.datetime.now()
        try:
            await db.execute(statement)
            ping_db_time = datetime.datetime.now() - start
            return ping_db_time
        except (exc.SQLAlchemyError, asyncpg.PostgresError) as err:
            return err.message

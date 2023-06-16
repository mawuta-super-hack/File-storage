import datetime
import secrets
import string
import sys
from typing import Annotated, Generic, List, Optional, Type, TypeVar

import asyncpg
from fastapi import Depends, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from core.config import app_settings
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


class RepositoryDBFiles(
    Repository, Generic[ModelType, CreateSchemaType]):
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
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = FileModel(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(
                self,
                db: AsyncSession,
                path: str,
                id: str 
                # path & id query param
    ) -> ModelType:
        """Download a file."""
        print(path, id)
        if id:
            statement = select(self._model).where(self._model.id == id)
        else:
            statement = select(self._model).where(self._model.path == path)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def ping_db(self,
            db: AsyncSession):
        """Return ping db time."""
        statement = text('SELECT version();')
        start = datetime.datetime.now()
        try:
            await db.execute(statement)
            ping_db_time = datetime.datetime.now() - start
            return ping_db_time
        except (exc.SQLAlchemyError, asyncpg.PostgresError) as err:
            return err.message

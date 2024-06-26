
from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy_utils import UUIDType

from db.db import Base


class FileModel(Base):
    """Data about files."""
    __tablename__ = 'files'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    name = Column(String(100))
    size = Column(Integer, default=0)
    path = Column(String(250), unique=True)
    is_downloadable = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    author = Column(UUIDType(binary=False), default=uuid4)

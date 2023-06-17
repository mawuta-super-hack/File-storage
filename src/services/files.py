
from models.db_models import FileModel
from schemas.db_schemas import FileCreate

from .base import RepositoryDBFiles


class RepositoryFiles(RepositoryDBFiles[FileModel, FileCreate]):
    pass


file_crud = RepositoryFiles(FileModel)

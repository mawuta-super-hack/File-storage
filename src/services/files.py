
from models.db_models import FileModel
from schemas.db_schemas import FileCreate

from .base import RepositoryDBFiles


class RepositoryFiles(RepositoryDBFiles[FileModel, FileCreate]):
    pass


#class RepositoryUsers(RepositoryDBUsers[UserModel, UserRegister]):
#    pass


file_crud = RepositoryFiles(FileModel)
#user_crud = RepositoryUsers(UserModel)

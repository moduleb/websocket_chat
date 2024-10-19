from app.db.database import get_session
from app.db.models.user import User
from app.services.crud_service import CrudService
from app.services.sessions.session_service import session_service
from app.services.user_service import UserService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


class ServiceFactory:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    def get_user_service(self):
        user_crud = CrudService(self.db_session, User)
        return UserService(user_crud)

    # def get_msg_service(self):
    #     user_crud = CrudService(self.db_session, Msg)
    #     return MsgService(user_crud)

    def get_session_service(self):
        return session_service




def get_service_factory(db_session: AsyncSession = Depends(get_session)):
    return ServiceFactory(db_session)

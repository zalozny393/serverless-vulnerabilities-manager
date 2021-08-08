from typing import Iterable

from src.models.user import User
from src.services.database_service import DatabaseService


class UserService:
    def __init__(self):
        self.database_service = DatabaseService()

    def get_user_groups(self, username: str) -> Iterable:
        user = User(username=username)

        user_data = self.database_service.get_item(pk_value=user.sk)
        user = User.from_item(user_data)

        return user.groups

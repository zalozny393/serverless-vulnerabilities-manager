from typing import Iterable

from src.models.user_model import UserModel
from src.services.database_service import DatabaseService


class UserService:
    def __init__(self):
        self.database_service = DatabaseService()

    def get_user(self, username):
        user = UserModel(username=username)

        user_data = self.database_service.get_item(pk_value=user.sk)
        return UserModel.from_item(user_data)

    def get_user_groups(self, username: str) -> Iterable:
        user = UserModel(username=username)

        user_data = self.database_service.get_item(pk_value=user.sk)
        user = UserModel.from_item(user_data)

        return user.groups

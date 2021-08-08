from typing import Iterable

from src.models.group import Group
from src.models.user import User
from src.services.database_service import DatabaseService, SORT_KEY, GLOBAL_SECONDARY_INDEX


class UserService:
    def __init__(self):
        self.database_service = DatabaseService()

    def get_user_groups(self, username: str) -> Iterable:
        user = User(username=username)

        users = self.database_service.query(
            pk_value=user.sk,
            pk=SORT_KEY,
            index_name=GLOBAL_SECONDARY_INDEX
        )

        for user_data in users:
            user = User.from_item(user_data)
            yield Group(user.group_name)

from src.models.group import Group
from src.models.user import User
from src.services.database_service import DatabaseService, SORT_KEY, GLOBAL_SECONDARY_INDEX


class UserService:
    def get_user_groups(self, username: str):
        database_service = DatabaseService()

        user = User(username=username)

        users = database_service.query(
            pk_value=user.sk,
            pk=SORT_KEY,
            index_name=GLOBAL_SECONDARY_INDEX
        )

        for user_data in users:
            user = User.from_item(user_data)
            yield Group(user.group_name)
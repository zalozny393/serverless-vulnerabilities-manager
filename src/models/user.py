from src.models.group import Group
from src.services.database_service import SORT_KEY, PRIMARY_KEY


class User(Group):
    SELECTOR = 'USER'

    def __init__(self, username: str, group: str = None, name: str = ''):
        super().__init__(group)
        self.username = username
        self.name = name
        self.type = User.SELECTOR.capitalize()

    @staticmethod
    def to_item(user: 'User') -> dict:
        return {**user.keys(), **{
            'name': user.name,
            'type': user.type
        }}

    @staticmethod
    def from_item(item: dict) -> 'User':
        return User(
            username=User.get_user_name_from_pk(item[SORT_KEY]),
            group=Group.get_group_name_from_pk(item[PRIMARY_KEY]),
            name=item.get('name')
        )

    @staticmethod
    def get_user_name_from_pk(sk: str) -> str:
        data = sk.split('#')
        if data[0] != User.SELECTOR:
            raise ValueError('Wrong Sort Key')

        return data[1]

    @property
    def sk(self) -> str:
        return f'{User.SELECTOR}#{self.username}'

from typing import List

from src.models.item import Item
from src.services.database_service import SORT_KEY


class UserModel(Item):
    SELECTOR = 'USER'

    def __init__(self, username: str, groups: List[str] = None, name: str = ''):
        super().__init__()
        self.username = username
        self.name = name
        self.groups = groups
        self.type = UserModel.SELECTOR.capitalize()

    @staticmethod
    def to_item(user: 'UserModel') -> dict:
        return {**user.keys(), **{
            'name': user.name,
            'type': user.type,
            'groups': user.groups,
        }}

    @staticmethod
    def from_item(item: dict) -> 'UserModel':
        return UserModel(
            username=UserModel.get_user_name_from_pk(item[SORT_KEY]),
            groups=item.get('groups'),
            name=item.get('name')
        )

    @staticmethod
    def get_user_name_from_pk(sk: str) -> str:
        data = sk.split('#')
        if data[0] != UserModel.SELECTOR:
            raise ValueError('Wrong Sort Key')

        return data[1]

    @property
    def pk(self) -> str:
        return f'{UserModel.SELECTOR}#{self.username}'

    @property
    def sk(self) -> str:
        return f'{UserModel.SELECTOR}#{self.username}'

from src.models.item import Item
from src.services.database_service import PRIMARY_KEY


class GroupModel(Item):
    SELECTOR = 'GROUP'

    def __init__(self, name: str):
        super().__init__()
        self.type = GroupModel.SELECTOR.capitalize()
        self.name = name

    @staticmethod
    def to_item(group: 'GroupModel') -> dict:
        return {**group.keys(), **{
            'type': group.type
        }}

    @staticmethod
    def from_item(item: dict) -> 'GroupModel':
        return GroupModel(
            name=GroupModel.get_group_name_from_pk(item[PRIMARY_KEY])
        )

    @staticmethod
    def get_group_name_from_pk(pk: str) -> str:
        data = pk.split('#')
        if data[0] != GroupModel.SELECTOR:
            raise ValueError('Wrong Primary Key')

        return data[1]

    @staticmethod
    def generate_pk(group_name: str) -> str:
        return f'{GroupModel.SELECTOR}#{group_name}'

    @property
    def pk(self) -> str:
        return GroupModel.generate_pk(self.name)

    @property
    def sk(self) -> str:
        return self.pk

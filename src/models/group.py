from src.models.item import Item
from src.services.database_service import PRIMARY_KEY


class Group(Item):
    SELECTOR = 'GROUP'

    def __init__(self, name: str):
        super().__init__()
        self.type = Group.SELECTOR.capitalize()
        self._name = name

    @staticmethod
    def to_item(group: 'Group'):
        return {**group.keys(), **{
            'type': group.type
        }}

    @staticmethod
    def from_item(item: dict):
        return Group(
            name=Group.get_group_name_from_pk(item[PRIMARY_KEY])
        )

    @staticmethod
    def get_group_name_from_pk(pk: str):
        data = pk.split('#')
        if data[0] != Group.SELECTOR:
            raise ValueError('Wrong Primary Key')

        return data[1]

    @property
    def pk(self) -> str:
        return f'{Group.SELECTOR}#{self._name}'

    @property
    def sk(self) -> str:
        return self.pk

    @property
    def group_name(self):
        return self._name

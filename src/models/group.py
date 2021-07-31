from src.models.item import Item


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

    @property
    def pk(self) -> str:
        return f'{Group.SELECTOR}#{self._name}'

    @property
    def sk(self) -> str:
        return self.pk

    @property
    def group_name(self):
        return self._name

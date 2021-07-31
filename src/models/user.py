from src.models.group import Group


class User(Group):
    SELECTOR = 'USER'

    def __init__(self, username: str, group: str = None, name: str = ''):
        super().__init__(group)
        self.username = username
        self.name = name
        self.type = User.SELECTOR.capitalize()

    @staticmethod
    def to_item(user: 'User'):
        return {**user.keys(), **{
            'name': user.name,
            'type': user.type
        }}

    @property
    def sk(self) -> str:
        return f'{User.SELECTOR}#{self.username}'

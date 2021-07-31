import os
import random

from faker import Faker

from src.models.group import Group
from src.models.user import User
from src.services.database import DatabaseService


if os.getenv('STAGE') == 'dev' and os.getenv('DEBUG') == 'true':
    print('Debug is on')
    import pydevd_pycharm
    pydevd_pycharm.settrace('localhost', port=8050, stdoutToServer=True, stderrToServer=True, suspend=False)
else:
    print('Debug is off')


TEST_DATA_DIR = 'test_data/'
GROUPS_FILE = f'{TEST_DATA_DIR}groups.json'
USERS_FILE = f'{TEST_DATA_DIR}users.json'
NUMBER_OF_GROUPS = 10
NUMBER_OF_USERS = 20


def load_test_data(event, _):
    database_service = DatabaseService()

    fake = Faker()
    groups = []
    for _ in range(NUMBER_OF_GROUPS):
        groups.append(Group(fake.company()))

    users = []
    for _ in range(NUMBER_OF_USERS):
        email = fake.email()
        name = fake.name()
        for group in random.sample(groups, random.randint(1, 5)):
            users.append(User(
                username=email,
                name=name,
                group=group.group_name
            ))

    database_service.batch_create(
        list(map(lambda group: Group.to_item(group), groups)) +
        list(map(lambda user: User.to_item(user), users))
    )


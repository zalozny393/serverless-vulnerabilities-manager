import os
import random
import uuid

from faker import Faker

from src.models.asset_vulnerability import AssetVulnerability
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
NUMBER_OF_ASSET_VULNERABILITIES = 100


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
    # add admin user
    for group in groups:
        users.append(User(
                username='admin@test.com',
                name='Admin',
                group=group.group_name
        ))

    asset_vulnerabilities = []
    ips = [fake.ipv4() for _ in range(20)]
    for _ in range(NUMBER_OF_ASSET_VULNERABILITIES):
        asset_vulnerabilities.append(AssetVulnerability(
            group=random.choice(groups).group_name,
            ip=random.choice(ips),
            severity=random.randint(0, 4),
            status=random.randint(0, 4),
            vulnerability_id=str(uuid.uuid4()),
            name=fake.sentences(nb=1)[0],
            description=fake.text()
        ))

    database_service.batch_create(
        list(map(lambda group: Group.to_item(group), groups)) +
        list(map(lambda user: User.to_item(user), users)) +
        list(map(lambda av: AssetVulnerability.to_item(av), asset_vulnerabilities))
    )

    print(f'Loaded: groups - {len(groups)}, users - {len(users)}, asset vulnerabilities - {len(asset_vulnerabilities)}')


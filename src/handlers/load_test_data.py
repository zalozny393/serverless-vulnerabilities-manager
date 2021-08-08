import random
import uuid
from typing import List

from faker import Faker

from src.models.asset_vulnerability import AssetVulnerability
from src.models.group import Group
from src.models.user import User
from src.services.database_service import DatabaseService
from src.utils.debugger import init_debug_mode

init_debug_mode()

NUMBER_OF_GROUPS = 5
NUMBER_OF_USERS = 20
NUMBER_OF_ASSET_VULNERABILITIES = 150


def load_test_data(event, _):
    database_service = DatabaseService()

    fake = Faker()
    groups = []
    for _ in range(NUMBER_OF_GROUPS):
        groups.append(Group(fake.company()))

    users = []
    for _ in range(NUMBER_OF_USERS):
        users.append(User(
            username=fake.email(),
            name=fake.name(),
            groups=list(_get_group_names(random.sample(groups, random.randint(1, 3))))
        ))

    # add admin user
    users.append(User(
            username='admin@test.com',
            name='Admin',
            groups=list(_get_group_names(groups))
    ))

    asset_vulnerabilities = []
    ips = [fake.ipv4() for _ in range(20)]
    for _ in range(NUMBER_OF_ASSET_VULNERABILITIES):
        asset_vulnerabilities.append(AssetVulnerability(
            group=random.choice(groups).name,
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


def _get_group_names(groups: List[Group]):
    for group in groups:
        yield group.name

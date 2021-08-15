import json
import os
import random
import uuid
from typing import List

import boto3
from faker import Faker

from src.models.asset_vulnerability_model import AssetVulnerabilityModel
from src.models.group_model import GroupModel
from src.models.user_model import UserModel
from src.services.database_service import DatabaseService
from src.utils.debugger import init_debug_mode

init_debug_mode()

NUMBER_OF_GROUPS = 5
NUMBER_OF_USERS = 20
NUMBER_OF_ASSET_VULNERABILITIES = 150

database_service = DatabaseService()
sqs = boto3.resource('sqs')


def load_meta_data(event, _):
    fake = Faker()
    groups = []
    for _ in range(NUMBER_OF_GROUPS):
        groups.append(GroupModel(fake.company()))

    users = []
    for _ in range(NUMBER_OF_USERS):
        users.append(UserModel(
            username=fake.email(),
            name=fake.name(),
            groups=list(_get_group_names(random.sample(groups, random.randint(1, 3))))
        ))

    # add admin user
    all_group_names = list(_get_group_names(groups))
    users.append(UserModel(
            username='admin@test.com',
            name='Admin',
            groups=all_group_names
    ))

    # save user and groups to DynamoDB
    database_service.batch_create(
        list(map(lambda group: GroupModel.to_item(group), groups)) +
        list(map(lambda user: UserModel.to_item(user), users))
    )

    print(f'Created: groups - {len(groups)}, users - {len(users)}')

    ips = [fake.ipv4() for _ in range(20)]
    # send AssetVulnerabilities to creation queue
    queue_name = os.getenv('QUEUE_URL')
    print(f'Sending messages to {queue_name} queue')
    queue = sqs.Queue(os.getenv('QUEUE_URL'))

    number_of_av = event.get('number_of_av', 150)
    for _ in range(number_of_av):
        queue.send_message(MessageBody=json.dumps({
            'group': random.choice(all_group_names),
            'ip': random.choice(ips),
            'severity': random.randint(0, 4),
            'status': random.randint(0, 4),
            'vulnerability_id': str(uuid.uuid4()),
            'name': fake.sentences(nb=1)[0],
            'description': fake.text()
        }))

    print(f'{number_of_av} messages are sent')


def _get_group_names(groups: List[GroupModel]):
    for group in groups:
        yield group.name


def load_asset_vulnerabilities(event, _):
    asset_vulnerabilities = []
    for record in event['Records']:
        av = json.loads(record['body'])
        asset_vulnerabilities.append(AssetVulnerabilityModel(
            group=av['group'],
            ip=av['ip'],
            severity=av['severity'],
            status=av['status'],
            vulnerability_id=av['vulnerability_id'],
            name=av['name'],
            description=av['description']
        ))

    database_service.batch_create(list(map(lambda av: AssetVulnerabilityModel.to_item(av), asset_vulnerabilities)))

    print(f'Created: asset vulnerabilities - {len(event["Records"])}')

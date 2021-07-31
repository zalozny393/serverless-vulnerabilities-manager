import os
from typing import Iterable

import boto3

from src.models.item import Item

dynamodb = boto3.resource('dynamodb')


class DatabaseService:
    def __init__(self):
        self.table = dynamodb.Table(os.environ.get('TABLE_NAME'))

    def create(self, item: Item):
        self.table.put_item(Item=item)

    def batch_create(self, items: Iterable[any]):
        counter = 0
        with self.table.batch_writer() as batch:
            for item in items:
                counter += 1
                batch.put_item(Item=item)

        print(f'{counter} records created')

    def select(self):
        pass

    def delete(self):
        pass

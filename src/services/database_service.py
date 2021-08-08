import os
from typing import Iterable

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
PRIMARY_KEY = 'PK'
SORT_KEY = 'SK'
GLOBAL_SECONDARY_INDEX = 'GSI1'


class DatabaseService:
    def __init__(self):
        self.table = dynamodb.Table(os.environ.get('TABLE_NAME'))

    def create(self, item: any) -> None:
        self.table.put_item(Item=item)

    def batch_create(self, items: Iterable[any]) -> None:
        counter = 0
        with self.table.batch_writer() as batch:
            for item in items:
                counter += 1
                batch.put_item(Item=item)

        print(f'{counter} records created')

    def get_item(self, pk_value: str, sk_value: str = None, pk_key: str = PRIMARY_KEY, sk_key: str = SORT_KEY):
        if not sk_value:
            sk_value = pk_value
        item = self.table.get_item(
            Key={
                pk_key: pk_value,
                sk_key: sk_value
            }
        )
        return item['Item']

    def query(self,
              pk_value: str,
              pk: str = PRIMARY_KEY,
              sk: str = SORT_KEY,
              sk_value: str = None,
              index_name: str = None
              ) -> Iterable:
        expression = Key(pk).eq(pk_value) & Key(sk).eq(sk_value) if sk_value else Key(pk).eq(pk_value)

        kwargs = {}
        if index_name:
            kwargs['IndexName'] = index_name
        response = self.table.query(KeyConditionExpression=expression, **kwargs)

        return response['Items']

    def delete(self):
        pass

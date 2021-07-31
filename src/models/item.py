import json
from abc import ABC, abstractmethod
from typing import Iterable


class Item(ABC):
    def __init__(self, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def to_item(item: any):
        pass

    @classmethod
    def load_from_json(cls, json_data: str) -> Iterable['Item']:
        items = json.loads(json_data)
        for item in items:
            yield cls(**item)

    @classmethod
    def get_batch_keys(cls, items: Iterable['Item']) -> Iterable[any]:
        for item in items:
            yield cls.to_item(item)

    @property
    @abstractmethod
    def pk(self):
        pass

    @property
    @abstractmethod
    def sk(self):
        pass

    def keys(self):
        return {
            'PK': self.pk,
            'SK': self.sk,
        }

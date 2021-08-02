from abc import ABC, abstractmethod

from src.services.database_service import PRIMARY_KEY, SORT_KEY


class Item(ABC):
    def __init__(self, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def to_item(item: 'Item'):
        pass

    @staticmethod
    @abstractmethod
    def from_item(item: dict):
        pass

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
            PRIMARY_KEY: self.pk,
            SORT_KEY: self.sk,
        }

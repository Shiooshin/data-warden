import abc
from typing import Dict


class StorageHandler(abc.ABC):

    @abc.abstractmethod
    def write_repository_batch(self, date, data: Dict = dict()):
        pass

    @abc.abstractmethod
    def write_statistics_batch(self, date, data: Dict = dict()):
        pass

    @abc.abstractmethod
    def read_repository_batch(self, date, keys: list = list()):
        pass

    @abc.abstractmethod
    def read_statistics_batch(self, date, keys: list = list()):
        pass

    @abc.abstractmethod
    def connection_established(self):
        pass

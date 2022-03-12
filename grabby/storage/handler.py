import abc
from typing import Dict


class StorageHandler(abc.ABC):
    @abc.abstractmethod
    def write_batch(self, data: Dict = dict()):
        pass

    @abc.abstractmethod
    def get_batch(self, keys: Dict = list()):
        pass

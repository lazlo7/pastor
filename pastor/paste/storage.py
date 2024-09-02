from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def read(self, key: str) -> str | None:
        pass


    @abstractmethod
    def write(self, key: str, value: str):
        pass

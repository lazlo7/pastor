from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def read(self, paste_id: str) -> str | None:
        pass


    @abstractmethod
    def write(self, paste_id: str, text: str):
        pass

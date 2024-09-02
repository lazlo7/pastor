from pastor.paste.storage import Storage
import os.path


class PersistentStorage(Storage):
    def __init__(self, path: str):
        self.__path = path


    def __get_key_path(self, key: str) -> str:
        return os.path.join(self.__path, key) 


    def read(self, key: str) -> str | None:
        """
        Returns the content of a key.
        It is assumed that the key has been sanitized.
        """
        key_path = self.__get_key_path(key)
        try:
            with open(key_path, "r") as f:
                return f.read()
        except:
            return None


    def write(self, key: str, value: str):
        """
        writes the content of a key.
        It is assumed that the key has been sanitized.
        """
        os.makedirs(self.__path, exist_ok=True)
        key_path = self.__get_key_path(key)
        with open(key_path, "w") as f:
            f.write(str(value))

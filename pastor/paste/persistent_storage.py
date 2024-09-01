from pastor.paste.storage import Storage
import os.path


class PersistentStorage(Storage):
    def __init__(self, path: str):
        self.__path = path


    def __get_paste_path(self, paste_id: str) -> str:
        return os.path.join(self.__path, paste_id) 


    def read(self, paste_id: str) -> str | None:
        """
        Returns the content of a paste.
        It is assumed that the paste_id has been sanitized.
        """
        paste_path = self.__get_paste_path(paste_id)
        try:
            with open(paste_path, "r") as f:
                return f.read()
        except:
            return None


    def write(self, paste_id: str, text: str):
        """
        writes the content of a paste.
        It is assumed that the paste_id has been sanitized.
        """
        paste_path = self.__get_paste_path(paste_id)
        with open(paste_path, "w") as f:
            f.write(text)

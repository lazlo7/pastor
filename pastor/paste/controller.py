from pastor.paste.storage import Storage
from sqids.sqids import Sqids


class PasteController:
    # standard base64 alphabet, not using external definitions to avoid dependencies    
    __alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"
    __id_min_length = 6

    
    def __init__(self, sequential_id: int, storage: Storage):
        self.__storage = storage
        self.__seq_id = sequential_id
        self.__sqids = Sqids(alphabet=PasteController.__alphabet, 
                             min_length=PasteController.__id_min_length)


    def __save_paste(self, paste_id: str, text: str):
        self.__storage.write(paste_id, text)


    def create_paste(self, text: str) -> str:
        paste_id = self.__sqids.encode([self.__seq_id])
        self.__seq_id += 1
        self.__save_paste(paste_id, text)
        return paste_id
    

    def get_paste(self, paste_id: str) -> str | None:
        return self.__storage.read(paste_id)

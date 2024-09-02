from pastor.paste.storage import Storage
from sqids.sqids import Sqids


class PasteController:
    # standard base64 alphabet, not using external definitions to avoid dependencies    
    __alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"
    __id_min_length = 6
    __seq_id_key = "$seqid"

    
    def __init__(self, storage: Storage):
        self.__storage = storage
        self.__seq_id = self.__load_seq_id()
        self.__sqids = Sqids(alphabet=PasteController.__alphabet, 
                             min_length=PasteController.__id_min_length)


    def __load_seq_id(self) -> int:
        try:
            seqid = self.__storage.read(PasteController.__seq_id_key)
            if seqid is None:
                return 0
            return int(seqid)
        except ValueError:
            # TODO: add logging.
            return 0
        except:
            return 0


    def __update_seq_id(self):
        self.__seq_id += 1
        self.__storage.write(PasteController.__seq_id_key, 
                             str(self.__seq_id))


    def __save_paste(self, paste_id: str, text: str):
        self.__storage.write(paste_id, text)


    @staticmethod
    def is_paste_id_valid(paste_id: str) -> bool:
        # TODO: can be optimized: check character code ranges.
        return all(c in PasteController.__alphabet for c in paste_id) and \
               len(paste_id) >= PasteController.__id_min_length


    def create_paste(self, text: str) -> str:
        paste_id = self.__sqids.encode([self.__seq_id])
        self.__update_seq_id()
        self.__save_paste(paste_id, text)
        return paste_id
    

    def get_paste(self, paste_id: str) -> str | None:
        return self.__storage.read(paste_id)

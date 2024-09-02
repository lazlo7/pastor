from pastor.paste.controller import PasteController
from pastor.paste.persistent_storage import PersistentStorage
from pastor.config import APP_PASTE_STORAGE_PATH


storage = PersistentStorage(path=APP_PASTE_STORAGE_PATH)
controller = PasteController(storage)


def get_controller() -> PasteController: 
    return controller

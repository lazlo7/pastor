from starlette.config import Config


config = Config(".env")

APP_PASTE_STORAGE_PATH = config("APP_PASTE_STORAGE_PATH", default="/tmp/paste")

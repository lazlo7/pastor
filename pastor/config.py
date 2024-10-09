from starlette.config import Config


config = Config(".env")

APP_WEB_PORT      = config("APP_WEB_PORT", cast=int, default=8000)
POSTGRES_HOST     = config("POSTGRES_HOST", cast=str, default="localhost")
POSTGRES_PORT     = config("POSTGRES_PORT", cast=int, default=5432)
POSTGRES_USER     = config("POSTGRES_USER", cast=str, default="pastor")
POSTGRES_DB       = config("POSTGRES_DB", cast=str, default="pastor")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=str, default="YOUR_DATABASE_PASSWORD")

# TODO: add ability to explicitly set dsn.
DATABASE_DSN = "postgresql+psycopg://{user}:{password}@{host}:{port}/{name}".format(
    user=POSTGRES_USER, 
    password=POSTGRES_PASSWORD, 
    host=POSTGRES_HOST, 
    port=POSTGRES_PORT, 
    name=POSTGRES_DB
)

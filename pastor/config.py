from starlette.config import Config


config = Config(".env")

POSTGRES_HOST     = config("POSTGRES_HOST", default="localhost")
POSTGRES_PORT     = config("POSTGRES_PORT", default="8001")
POSTGRES_USER     = config("POSTGRES_USER", default="pastor")
POSTGRES_DB       = config("POSTGRES_DB", default="pastor")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", default="YOUR_DATABASE_PASSWORD")

# TODO: add ability to explicitly set dsn.
DATABASE_DSN = "postgresql+psycopg://{user}:{password}@{host}:{port}/{name}".format(
    user=POSTGRES_USER, 
    password=POSTGRES_PASSWORD, 
    host=POSTGRES_HOST, 
    port=POSTGRES_PORT, 
    name=POSTGRES_DB
)

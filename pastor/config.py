from starlette.config import Config


config = Config(".env")

APP_SEQID_PATH    = config("APP_SEQID_PATH", default="/tmp/seqid")
POSTGRES_HOST     = config("POSTGRES_HOST", default="localhost")
POSTGRES_PORT     = config("POSTGRES_PORT", default="8001")
POSTGRES_USER     = config("POSTGRES_USER", default="pastor")
POSTGRES_DB       = config("POSTGRES_DB", default="pastor")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", default="YOUR_DATABASE_PASSWORD")

# TODO: add ability to explicitly set dsn.
DATABASE_DSN = "postgresql://{user}:{password}@{host}:{port}/{name}".format(POSTGRES_USER, 
                                                                            POSTGRES_PASSWORD, 
                                                                            POSTGRES_HOST, 
                                                                            POSTGRES_PORT, 
                                                                            POSTGRES_DB)

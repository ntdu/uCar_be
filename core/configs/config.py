from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_HOST: str
    APP_PORT: int

    POSTGRES_HOST: str
    POSTGRES_DB: str
    DB_USER: str
    DB_PASSWORD: str
    DBTYPE: str

    CLIENT_ORIGIN: str

    class Config:
        env_file = './.env'


settings = Settings()


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    JWT_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


# print(settings.SQLALCHEMY_DATABASE_URL)
# print('-------------------------------------------------------------')
# print('-------------------------------------------------------------')
# print(settings.JWT_SECRET_KEY)

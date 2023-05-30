from pydantic import BaseConfig, BaseSettings, Field


class Env(BaseSettings):
    """Environment variables"""

    class Config(BaseConfig):
        """Config"""

        env_file = ".env"
        env_file_encoding = "utf-8"

    HTTP_URL: str = Field(..., env="HTTP_URL")
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


env = Env()

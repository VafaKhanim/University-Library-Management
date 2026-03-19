from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    DATABASE_URL: str
    FIRST_ADMIN_USERNAME: str = "admin" #defauldu
    FIRST_ADMIN_PASSWORD: str = "admin123" #bunu da

    class Config:
        env_file = ".env"


# burda singleton pattern mentiqi istifade etmishem — yalnız bir settings instansiyası
settings = Settings()
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

    HOST: str
    PORT: int
    SERVICE_WORKERS: int
    THREAD_SIZE: int

class DBConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

    HOST: str
    PORT: str
    USER: str
    PASS: str
    NAME: str
    POOL_SIZE: int

    @property
    def DATABASE_URL(self):
        return f"postgresql+psycopg2://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"

class ParamConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PARAM_",
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

    OTP_LENGTH: int
    OTP_REQ_LIMIT: int
    OTP_VALIDATE_LIMIT: int
    OTP_REQ_COOLDOWN_HOURS: int
    OTP_VALIDATE_COOLDOWN_HOURS: int
    OTP_CODE_EXPIRED_MINUTES: int

    WA_SENDER_URL: str
    WA_PROJECT_ID: str
    WA_TYPE: str

    REQUEST_TIMEOUT: int

APP_CONFIG = AppConfig()
DB_CONFIG = DBConfig()
PARAM_CONFIG = ParamConfig()

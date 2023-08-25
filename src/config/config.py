"""src/confid/config.py"""

from pathlib import Path

from passlib.context import CryptContext
from pydantic import BaseConfig, BaseModel, BaseSettings


# API Settings
class APIUrlsSettings(BaseModel):
    """Configure public urls."""

    docs: str = "/docs"
    redoc: str = "/redoc"


class PublicApiSettings(BaseModel):
    """Configure public API settings."""

    name: str = "FastAPI Store"
    urls: APIUrlsSettings = APIUrlsSettings()


# Database Settings
class DatabaseSettings(BaseModel):
    """Configure SQLite3 Database settings."""

    name: str = "db.sqlite3"

    @property
    def url(self) -> str:
        return f"sqlite+aiosqlite:///./{self.name}"


# Kafka Settings
class KafkaSettings(BaseModel):
    """Configure Kafka settings."""

    bootstrap_servers: str = "localhost:9092"


# Logging Settings
class LoggingSettings(BaseModel):
    """Configure the logging engine."""

    # The time field can be formatted using more human-friendly tokens.
    # These constitute a subset of the one used by the Pendulum library
    # https://pendulum.eustace.io/docs/#tokens
    format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level: <5} | {message}"

    # The .log filename
    file: str = "backend"

    # The .log file Rotation
    rotation: str = "1MB"

    # The type of compression
    compression: str = "zip"


# Authentication Settings
class AccessTokenSettings(BaseModel):
    """Configure Token settings."""

    secret_key: str = "invaliad"
    ttl: int = 3600  # seconds


class RefreshTokenSettings(BaseModel):
    """Configure Refresh Token settings."""

    secret_key: str = "invaliad"
    ttl: int = 3600  # seconds


class AuthenticationSettings(BaseModel):
    """Configure Authentication settings."""

    access_token: AccessTokenSettings = AccessTokenSettings()
    refresh_token: RefreshTokenSettings = RefreshTokenSettings()
    algorithm: str = "HS256"
    scheme: str = "Bearer"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Settings are powered by pydantic
# https://pydantic-docs.helpmanual.io/usage/settings/
class Settings(BaseSettings):
    debug: bool = True

    # Project file system
    root_dir: Path
    src_dir: Path

    # Infrastructure settings
    database: DatabaseSettings = DatabaseSettings()

    # Application configuration
    public_api: PublicApiSettings = PublicApiSettings()
    logging: LoggingSettings = LoggingSettings()
    authentication: AuthenticationSettings = AuthenticationSettings()

    class Config(BaseConfig):
        env_nested_delimiter: str = "__"
        env_file: str = ".env"


# Define the root path
# ======================================
ROOT_PATH = Path(__file__).parent.parent

# ======================================
# Load settings
# ======================================
settings = Settings(
    # NOTE: The root and applications directories are hard-coded
    #       to avoid overriding via environment variables
    root_dir=ROOT_PATH,
    src_dir=ROOT_PATH / "src",
)

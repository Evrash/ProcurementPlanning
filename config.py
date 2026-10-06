from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'db.sqlite3'

class DbConfig(BaseModel):
    url: str
    echo: bool = False
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / '.env.template', BASE_DIR / '.env'),
        case_sensitive=False,
        env_nested_delimiter='__',
        env_prefix='APP_CONFIG__'
    )
    base_dir: Path = BASE_DIR
    db: DbConfig

settings = Settings()

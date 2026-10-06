from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'db.sqlite3'

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / '.env.template', BASE_DIR / '.env'),
        case_sensitive=False,
        env_nested_delimiter='__',
        env_prefix='APP_CONFIG__'
    )
    base_dir: Path = BASE_DIR
    db_url: str = f'sqlite+aiosqlite:///{DB_PATH}'

settings = Settings()

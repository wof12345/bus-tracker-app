import logging
import os
from functools import lru_cache
from logging.handlers import RotatingFileHandler

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    database_url: str
    database_name: str = 'vehicle_tracker_app'
    secret: str
    jwt_secret: str
    port: int = 8001

    class Config:
        env_file = '.env'


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()


def configure_logging():
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger('watchfiles.main')
    logger.setLevel(logging.WARNING)

    logging.basicConfig(
        level=logging.INFO if not settings.debug else logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                'logs/app.log', maxBytes=10 * 1024 * 1024, backupCount=5
            ),
            logging.StreamHandler(),
        ],
    )

    return logging.getLogger(__name__)


logger = configure_logging()

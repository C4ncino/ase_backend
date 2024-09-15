import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


# Configura la aplicación Flask.
class AppConfig:
    DEBUG = bool(os.getenv('DEBUG', 1))
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = os.getenv('PORT', 5000)

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 1))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 30))
    )

    CELERY_BROKER_URL = os.getenv(
        'CELERY_BROKER_URL', 'redis://localhost:6379/0'
    )
    CELERY_RESULT_BACKEND = os.getenv(
        'CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'
    )

    CELERY = dict(
        broker_url=CELERY_BROKER_URL,
        result_backend=CELERY_RESULT_BACKEND,
        task_ignore_result=True
    )


# Utiliza get_db_url() para construir la URL de conexión a la base de datos.
class DatabaseConfig:
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')

    @classmethod
    def get_db_url(self, db_prefix='postgresql://') -> str:
        """Returns the url to connect to the database"""
        url = db_prefix + self.DB_USER + ':' + self.DB_PASSWORD + \
            '@' + self.DB_HOST + ':' + self.DB_PORT + '/' + self.DB_NAME

        return url

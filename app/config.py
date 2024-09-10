import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


# Configura la aplicación Flask.
class AppConfig:
    DEBUG = 1
    HOST = os.getenv('HOST', '172.18.26.235')
    PORT = os.getenv('PORT', 5000)

    SERVER_NAME = f'{HOST}:{PORT}'

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 1)
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 30)
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

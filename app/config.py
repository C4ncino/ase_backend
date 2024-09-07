import os
from dotenv import load_dotenv

load_dotenv()


class AppConfig:# Configura la aplicación Flask.
    DEBUG = 1
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = os.getenv('PORT', 5000)

    SERVER_NAME = f'{HOST}:{PORT}'

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


class DatabaseConfig:# Utiliza get_db_url() para construir la URL de conexión a la base de datos.
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

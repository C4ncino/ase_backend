from . import app
from .config import AppConfig

if __name__ == '__main__':
    app.run(debug=AppConfig.DEBUG, host=AppConfig.HOST, port=AppConfig.PORT)

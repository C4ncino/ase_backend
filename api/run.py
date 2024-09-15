from app import app
from app.config import AppConfig

if __name__ == '__main__':
    app.run(debug=AppConfig.DEBUG, host=AppConfig.HOST, port=AppConfig.PORT)

from flixify.config import config
from flixify.server import create_app


app = create_app(config)

if __name__ == '__main__':
    app.run()

from flixify.config import config
from flixify.server import create_app
from flixify.setup.db import db

if __name__ == '__main__':
    app = create_app(config)
    with app.app_context():
        db.create_all()

from flixify.setup.db.models.base import Base
from flixify.setup.db import db


class User(Base):
    __tablename__ = 'user'
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    favorite_genre = db.Column(db.String)

from flixify.setup.db.base import Base
from flixify.setup.db import db


class Genre(Base):
    __tablename__ = 'genre'
    name = db.Column(db.String(100), unique=True, nullable=False)

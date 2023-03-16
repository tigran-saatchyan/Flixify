from flixify.setup.db import db
from flixify.setup.db.base import Base
from flixify.setup.db.director import Director
from flixify.setup.db.genre import Genre


class Movie(Base):
    __tablename__ = 'movie'
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    trailer = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    genre_id = db.Column(
        db.Integer,
        db.ForeignKey('genre.id'),
        nullable=False
    )
    genre = db.relationship(Genre)

    director_id = db.Column(
        db.Integer,
        db.ForeignKey('director.id'),
        nullable=False
    )
    director = db.relationship(Director)

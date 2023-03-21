from flixify.setup.db.models.base import Base
from flixify.setup.db import db


class Director(Base):
    __tablename__ = 'director'
    name = db.Column(db.String(100), unique=True, nullable=False)

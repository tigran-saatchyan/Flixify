from flixify.setup.db import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated = db.Column(
        db.DateTime, default=db.func.now(),
        onupdate=db.func.now()
    )

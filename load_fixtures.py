from contextlib import suppress
from typing import Any, Dict, List, Type

from sqlalchemy.exc import IntegrityError

from flixify.config import config
from flixify.helpers.utils import read_json
from flixify.server import create_app
from flixify.setup.db import db
from flixify.setup.db.models import Base, Director, Genre, Movie


def load_data(data: List[Dict[str, Any]], model: Type[Base]) -> None:
    for item in data:
        item['id'] = item.pop('pk')
        db.session.add(model(**item))


if __name__ == '__main__':
    fixtures: Dict[str, List[Dict[str, Any]]] = read_json(
        "data/fixtures.json"
    )

    app = create_app(config)

    with app.app_context():
        load_data(fixtures['directors'], Director)
        load_data(fixtures['movies'], Movie)
        load_data(fixtures['genres'], Genre)

        with suppress(IntegrityError):
            db.session.commit()

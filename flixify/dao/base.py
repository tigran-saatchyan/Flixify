from typing import Generic, Optional, Type, TypeVar

from flask import current_app
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound

from flixify.setup.db.models import Base

T = TypeVar('T', bound=Base)


class BaseDAO(Generic[T]):
    __model__ = Base

    def __init__(self, session: scoped_session) -> None:
        self.db_session = session

    @property
    def _items_per_page(self) -> int:
        return current_app.config['MOVIES_PER_PAGE']

    def create(self, data: dict) -> None:
        entity = self.__model__(**data)

        self.db_session.add(entity)
        self.db_session.commit()

    def get_by_id(self, pk: int) -> Optional[T]:
        return self.db_session.query(self.__model__).get(pk)

    def get_all(
        self,
        page: Optional[int] = None,
        year: Optional[int] = None,
        did: Optional[int] = None,
        gid: Optional[int] = None,
        status: Optional[str] = None
    ) -> list[Type[Base]]:

        req: BaseQuery[Base] = self.db_session.query(self.__model__)

        if year:
            req = req.filter(self.__model__.year == year)

        if did:
            req = req.filter(self.__model__.director_id == did)

        if gid:
            req = req.filter(self.__model__.genre_id == gid)

        if status == 'new':
            req = req.order_by(self.__model__.year.desc())

        if page:
            try:
                return req.paginate(
                    page=page,
                    per_page=self._items_per_page,
                    error_out=False
                ).items
            except NotFound:
                return []
        return req.all()

    def update(self, pk: int, data: dict) -> int:

        row_updated = self.db_session.query(self.__model__).filter(
            self.__model__.id == pk
        ).update(data)

        self.db_session.commit()

        return row_updated

    def delete(self, pk: int) -> None:
        director = self.get_by_id(pk)
        self.db_session.delete(director)
        self.db_session.commit()

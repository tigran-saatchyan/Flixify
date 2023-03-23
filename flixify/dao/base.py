from typing import Generic, Optional, Type, TypeVar

from flask import current_app
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound

from flixify.helpers.log_handler import dao_logger
from flixify.setup.db.models import Base

T = TypeVar('T', bound=Base)


class BaseDAO(Generic[T]):
    __model__ = Base

    def __init__(self, session: scoped_session) -> None:
        self.db_session = session
        self.logger = dao_logger

    @property
    def _items_per_page(self) -> int:
        return current_app.config['MOVIES_PER_PAGE']

    def create(self, data: dict) -> None:
        entity = self.__model__(**data)

        self.db_session.add(entity)
        self.db_session.commit()
        self.logger.debug(f"Created entity with data: {data['email']}")

    def get_by_id(self, pk: int) -> Optional[T]:
        result = self.db_session.query(self.__model__).get(pk)
        if result:
            self.logger.info(f"Retrieved entity with primary key: {pk}")
        else:
            self.logger.info(f"No entity found with primary key: {pk}")
        return result

    def get_all(
        self,
        page: Optional[int] = None,
        year: Optional[int] = None,
        did: Optional[int] = None,
        gid: Optional[int] = None,
        status: Optional[str] = None
    ) -> list[Type[Base]]:
        self.logger.info("Getting all records from database.")
        req: BaseQuery[Base] = self.db_session.query(self.__model__)

        if year:
            req = req.filter(self.__model__.year == year)
            self.logger.info(f"Filtering by year: {year}")

        if did:
            req = req.filter(self.__model__.director_id == did)
            self.logger.info(f"Filtering by director_id: {did}")

        if gid:
            req = req.filter(self.__model__.genre_id == gid)
            self.logger.info(f"Filtering by genre_id: {gid}")

        if status == 'new':
            req = req.order_by(self.__model__.year.desc())
            self.logger.info("Sorting by year in descending order.")

        if page:
            try:
                items = req.paginate(
                    page=page,
                    per_page=self._items_per_page,
                    error_out=False
                ).items
                self.logger.info(
                    f"Retrieved page {page} with {len(items)} "
                    f"items."
                    )
                return items
            except NotFound:
                self.logger.warning(f"Page {page} not found.")
                return []

        items = req.all()
        self.logger.info(f"Retrieved all records: {len(items)}")
        return items

    def update(self, pk: int, data) -> None:
        self.logger.info(f"Updating record with id {pk}.")
        self.db_session.query(self.__model__).filter(
            self.__model__.id == pk
        ).update(data)
        self.db_session.commit()
        self.logger.info(f"Record with id {pk} updated successfully.")

    def delete(self, pk: int) -> None:
        self.logger.info(f"Deleting record with id {pk}.")
        director = self.get_by_id(pk)
        self.db_session.delete(director)
        self.db_session.commit()
        self.logger.info(f"Record with id {pk} deleted successfully.")

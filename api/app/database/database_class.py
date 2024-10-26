from app.config import DatabaseConfig
from datetime import datetime as dt
from threading import Lock

import sqlalchemy.exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry

from .models.base import Base, AbstractModel
from .models.users import User
from .models.words import Word
from .models.data_words import Data
from .models.user_models import Model


class Query(dict):
    field: str
    value: str | int | float | bool | dt
    comparison: str


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance

        return cls._instances[cls]


class DatabaseInterface(metaclass=SingletonMeta):
    """
    DB Interface with SQLAlchemy and PostgreSQL

    methods:
        create_table_row(table_name: str, row_info: dict)
        read_all_table(table_name: str)
        read_by_id(table_name: str, element_id: int | str)
        read_by_field(table_name: str, field: str, value: str, comparison='eq')
        read_by_fields(table_name: str, queries: list[Query])
        update_table_row(table_name: str, element_id: int | str, row_info: dict) # noqa
        delete_table_row(table_name: str, id_element: int | str)

    attributes:
        __engine: The engine to connect to the database
        __session: The session to connect to the database
        __TABLE_CLASS_MAP: The map of table classes
    """

    __TABLE_CLASS_MAP = {
        'users': User,
        'models': Model,
        'words': Word,
        'data_words': Data,
    }

    def __init__(self) -> None:
        self.__engine = create_engine(DatabaseConfig.get_db_url(), echo=False)

        session_class = sessionmaker(bind=self.__engine)

        self.__session = session_class()

        mapper = registry()

        mapper.configure()

        Base.metadata.create_all(self.__engine)

    def create_table_row(self, table_name: str, row_info: dict) -> tuple[bool, AbstractModel]:
        """
        Create a new row in the table

        Parameters:
            table_name: The name of the table
            row_info: The info of the row

        Returns:
            bool: True if the row was created, False otherwise
        """

        table_class = self.__TABLE_CLASS_MAP.get(table_name.lower())

        if table_class:
            row = table_class(**row_info)
            self.__session.add(row)
            self.__session.commit()

            return True, row

        return False, None

    def read_all_table(self, table_name: str) -> list[AbstractModel]:
        """
        Read all rows in the table
        """

        table_class = self.__TABLE_CLASS_MAP.get(table_name.lower())

        if table_class:
            data = self.__session.query(table_class).all()

            return data if len(data) > 0 else []

        return []

    def read_by_id(self, table_name: str, element_id: int | str) -> AbstractModel | None:
        """
        Read a row by id

        Parameters:
            table_name: The name of the table
            element_id: The id of the element

        Returns:
            object: The row
        """

        table_class = self.__TABLE_CLASS_MAP.get(table_name.lower())

        if table_class:
            data = self.__session.query(table_class)

            return data.filter(table_class.id == element_id).first()

        return None

    def __filter_data(
        self,
        table_class: any,
        field: str,
        value: str | int | float | bool | dt,
        comparison='eq',
        data=None
    ):
        """
        Filter data

        Parameters:
            table_class: The class of the table
            field: The name of the field
            value: The value of the field
            comparison: The comparison operator
            data: The data to filter

        Returns:
            object: The filtered data
        """
        if data is None:
            data = self.__session.query(table_class)

        match comparison:
            case 'eq':
                data = data.filter(getattr(table_class, field) == value)
            case 'ne':
                data = data.filter(getattr(table_class, field) != value)
            case 'lt':
                data = data.filter(getattr(table_class, field) < value)
            case 'gt':
                data = data.filter(getattr(table_class, field) > value)
            case 'lte':
                data = data.filter(getattr(table_class, field) <= value)
            case 'gte':
                data = data.filter(getattr(table_class, field) >= value)

        return data

    def read_by_field(
        self, table_name: str, field: str, value: str, comparison='eq'
    ) -> list[AbstractModel]:
        """
        Read all rows by a selected field

        Parameters:
            table_name: The name of the table
            field: The name of the field
            value: The field value
            comparison: The comparison operator

        Returns:
            List of rows
        """

        table_class = self.__TABLE_CLASS_MAP.get(table_name.lower())

        if table_class:
            data = self.__filter_data(table_class, field, value, comparison)

            data = data.all()

            return data if len(data) > 0 else []

        return []

    def read_by_fields(self, table_name: str, queries: list[Query]) -> list[AbstractModel]:
        """
        Read all rows by a selected fields

        Parameters:
            table_name: The name of the table
            queries: The queries to perform

        Returns:
            List of rows
        """

        table_class = self.__TABLE_CLASS_MAP.get(table_name.lower())

        if table_class:
            data = self.__session.query(table_class)

            for query in queries:
                data = self.__filter_data(
                    table_class,
                    query['field'],
                    query['value'],
                    query['comparison'],
                    data=data,
                )

            data = data.all()

            return data if len(data) > 0 else []

        return []

    def update_table_row(
        self, table_name: str, element_id: int | str, row_info: dict
    ) -> AbstractModel | None:
        """
        Update a row by id

        Parameters:
            table_name: The name of the table
            element_id: The id of the element
            row_info: The info of the row

        Returns:
            object: The row
        """

        table_class = self.__TABLE_CLASS_MAP.get(table_name.lower())

        if table_class:
            data = self.__session.query(table_class)
            data = data.filter(table_class.id == element_id).first()

            for key, value in row_info.items():
                setattr(data, key, value)
            self.__session.commit()

            return data

        return None

    def delete_table_row(self, table_name: str, id_element: int | str) -> bool:
        """
        Delete a row by id

        Parameters:
            table_name: The name of the table
            id_element: The id of the element

        Returns:
            bool: True if the row was deleted, False otherwise
        """

        table_class = self.__TABLE_CLASS_MAP.get(table_name.lower())

        if table_class:
            try:
                data = self.__session.query(table_class)
                data = data.filter(table_class.id == id_element).first()

                self.__session.delete(data)
                self.__session.commit()

            except sqlalchemy.exc.SQLAlchemyError:
                return False

            return True

        return False

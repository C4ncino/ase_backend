"""
Initialize the Base for the models and database
"""
from sqlalchemy.ext.declarative import declarative_base
from abc import abstractmethod

Base = declarative_base()


class AbstractModel(Base):

    __abstract__ = True

    @abstractmethod
    def serialize(self) -> dict:
        pass

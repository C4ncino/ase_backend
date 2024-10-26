"""
Initialize the Base for the models and database
"""
from sqlalchemy.ext.declarative import declarative_base
from abc import ABC, abstractmethod

Base = declarative_base()


class AbstractModel(ABC):

    @abstractmethod
    def serialize(self) -> dict:
        pass

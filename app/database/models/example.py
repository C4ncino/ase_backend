from datetime import datetime as dt
from .base import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP


class Example(Base):
    """
    Example Model
    """

    __tablename__ = 'examples'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    creationDate = Column(TIMESTAMP(), nullable=False, default=dt.now())

    def serialize(self):
        """
        Serialize the data

        Returns:
            dict: The serialized data
        """

        return {
            "Id": self.id,
            "Name": self.name,
            "CreationDate": self.creationDate.strftime('%d-%m-%Y %H:%M:%S'),
        }

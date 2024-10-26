from datetime import datetime as dt
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, TIMESTAMP

from .base import AbstractModel


class User(AbstractModel):
    """
    Example Model
    """

    __tablename__ = "users"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    bday = Column(Date, nullable=False)
    password = Column(String(64), nullable=False)
    creationDate = Column(TIMESTAMP(), nullable=False, default=dt.now())

    words = relationship(
        "Word",
        back_populates="users",
        cascade="all, delete-orphan",
    )
    models = relationship(
        "Model",
        back_populates="users",
        cascade="all, delete-orphan",
    )

    def serialize(self):
        """
        Serialize the data

        Returns:
            dict: The serialized data

        """

        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "bday": self.bday,
            "creationDate": self.creationDate.strftime("%d-%m-%Y %H:%M:%S"),
        }

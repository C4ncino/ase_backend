from datetime import datetime as dt
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, JSON, ForeignKey, TIMESTAMP

from .base import AbstractModel


class Model(AbstractModel):
    """
    Word Model: Almacena palabras y datos de sensores asociados.
    """

    __tablename__ = "models"

    id = Column(Integer(), ForeignKey("users.id"), primary_key=True)
    last_update = Column(TIMESTAMP(), nullable=False, default=dt.now())
    model = Column(JSON, nullable=False)

    users = relationship("User", back_populates="models")

    def serialize(self):
        """
        Serialize the data

        Returns:
            dict: The serialized data
        """
        return {
            "id": self.id,
            "last_update": self.last_update.strftime("%d-%m-%Y %H:%M:%S"),
            "model": self.model,
        }

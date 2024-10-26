from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, JSON

from .base import AbstractModel


class Data(AbstractModel):
    __tablename__ = "data_words"

    id = Column(Integer, ForeignKey("words.id"),
                primary_key=True, nullable=False)
    data = Column(JSON, nullable=False)

    words = relationship("Word", back_populates="data_words")

    def serialize(self):
        """
        Serialize the data.

        Returns:
            dict: The serialized data
        """
        return {
            "id_word": self.id,
            "data": self.data,
        }

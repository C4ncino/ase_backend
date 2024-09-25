from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import Base

class Data(Base):
    __tablename__ = "data_words"

    id_word = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    users = relationship("User", back_populates="data_words")

    def serialize(self):
        """
        Serialize the data.

        Returns:
            dict: The serialized data
        """
        return {
            "id_word": self.id_word,
            "data": self.data,
        }

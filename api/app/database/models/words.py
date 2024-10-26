from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, JSON, ForeignKey

from .base import Base, AbstractModel


class Word(Base, AbstractModel):
    """
    Word Model: Almacena palabras y datos de sensores asociados.
    """

    __tablename__ = "words"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    class_key = Column(Integer, nullable=False)
    word = Column(String(50), nullable=False)
    characteristics = Column(JSON, nullable=False)
    model = Column(JSON, nullable=False)

    users = relationship("User", back_populates="words")
    data_words = relationship(
        "Data",
        back_populates="words",
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
            "word": self.word,
        }

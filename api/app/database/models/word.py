
from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Word(Base):
    """
    Word Model: Almacena palabras y datos de sensores asociados.
    """

    __tablename__ = "words"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    word = Column(String(50), nullable=False)
    # JSON para almacenar los datos del guante
    sensor_data = Column(JSON, nullable=False)
    # Relación con el usuario
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    users = relationship("User", back_populates="words")

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

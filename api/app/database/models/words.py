
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from .base import Base


class Word(Base):
    """
    Word Model: Almacena palabras y datos de sensores asociados.
    """

    __tablename__ = "words"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    word = Column(String(50), nullable=False)
    characteristics = Column(JSON, nullable=False)
    model = Column(LargeBinary, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    users = relationship("User", back_populates="words")
    datas = relationship(
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
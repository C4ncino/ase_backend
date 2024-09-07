#esta es la clase

from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    version = Column(String(50), nullable=False)
    blob_data = Column(LargeBinary, nullable=False)  # Para almacenar archivos tipo blob
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relación con la tabla User (padre)
    users = relationship("User", back_populates="models")

    def serialize(self):
        return {
            "id": self.id,
            "version": self.version,
            "user_id": self.user_id,
            # No incluimos el Blob en la serialización, pues es un archivo binario grande
        }

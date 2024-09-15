from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Model(Base):
    """
    Model: Stores file-related data.
    """
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(100), nullable=False)
    # Binary data for file content
    file_data = Column(LargeBinary, nullable=False)
    # Relación con el usuario
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    users = relationship("User", back_populates="models")

    def serialize(self):
        """
        Serialize the model data.

        Returns:
            dict: The serialized data
        """
        return {
            "id": self.id,
            "filename": self.filename,
        }

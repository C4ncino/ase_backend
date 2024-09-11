from sqlalchemy import Column, Integer, String, LargeBinary
from .base import Base  

class Model(Base):
    """
    Model: Stores file-related data.
    """
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(100), nullable=False)
    file_data = Column(LargeBinary, nullable=False)  # Binary data for file content

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

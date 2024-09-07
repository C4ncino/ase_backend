from datetime import datetime as dt
from .base import Base
from sqlalchemy import Column, Integer, String, Date, TIMESTAMP
from sqlalchemy.orm import relationship

class User(Base):
    """
    Example Model
    """

    __tablename__ = "users"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    bday = Column(Date, nullable=False)
    password = Column(String(60), nullable=False)
    creationDate = Column(TIMESTAMP(), nullable=False, default=dt.now())

    # Relacion con el modelo "words"
    words = relationship("Word", back_populates="users")  
     # Relación con el modelo 'Model'
    models = relationship("Model", back_populates="users", cascade="all, delete-orphan")

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

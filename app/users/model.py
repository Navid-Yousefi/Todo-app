from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher


pwd_context = PasswordHash((BcryptHasher(),))

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    tasks = relationship('TaskModel', back_populates='user')


    def hash_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)


    def verify_password(self,plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)


    def set_password(self, plain_text: str) -> None:
        self.password = self.hash_password(plain_text)
    
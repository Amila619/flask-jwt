from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Define the relationship to the Token class
    tokens = relationship("Token", back_populates="user")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


class Token(Base):
    __tablename__ = "TokenBlockList"

    id = Column(Integer, primary_key=True, nullable=False)
    jti = Column(String, nullable=False)
    token_type = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    revoked_at = Column(TIMESTAMP(timezone=True))
    expires = Column(TIMESTAMP(timezone=True), nullable=False)

    # Define the relationship to the User class
    user = relationship("User", back_populates="tokens")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

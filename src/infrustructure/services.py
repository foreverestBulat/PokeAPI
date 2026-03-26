# infrastructure/identity/jwt_service.py
from typing import Optional
from uuid import UUID, uuid4

import bcrypt
import jwt

from datetime import datetime, timedelta
from application.common.interfaces import IFileStorage, IJwtService, IPasswordHasher, TokenPayload
from domain.entities import User
from passlib.context import CryptContext

class JwtService(IJwtService):
    def __init__(self, secret: str, algorithm: str = "HS256"):
        self._secret = secret
        self._algorithm = algorithm

    def create_token(self, user: User) -> str:
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)
    
    def decode_token(self, token: str) -> Optional[TokenPayload]:
        try:
            payload = jwt.decode(
                token, 
                self._secret, 
                algorithms=[self._algorithm]
            )
            
            return TokenPayload(
                user_id=UUID(payload["sub"]),
                email=payload["email"]
            )
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, KeyError, ValueError):
            return None


class PasswordHasher(IPasswordHasher):
    def hash(self, password: str) -> str:
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pwd_bytes, salt)
        return hashed.decode('utf-8')

    def verify(self, password: str, hashed_password: str) -> bool:
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)


class LocalFileStorage(IFileStorage):
    async def upload(self, file_bytes: bytes, filename: str) -> str:
        unique_name = f"{uuid4()}_{filename}"
        path = f"media/avatars/{unique_name}"
        with open(path, "wb") as f:
            f.write(file_bytes)
        return path
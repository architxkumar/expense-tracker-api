import os
import time

import jwt


class JWTService:
    ALGORITHM = 'HS256'
    EXPIRATION_TIME = 3600
    @staticmethod
    def generate_token(user_id: str) -> str:
        secret = os.getenv('JWT_TOKEN')
        jwt_payload = {
            "sub": user_id,
            "exp": int(time.time()) + JWTService.EXPIRATION_TIME,
        }
        encoded = jwt.encode(jwt_payload, secret, JWTService.ALGORITHM)
        return encoded

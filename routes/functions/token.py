import jwt
from datetime import datetime, timedelta, timezone

import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

class Token:

    def auth(self, user_id):
        access_token = self.encode_access_token(user_id)
        refresh_token = self.encode_refresh_token(user_id)
        auth_obj = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        return auth_obj

    def encode_token(self, sub, expires_sec):
        try:
            payload = {
                'exp': datetime.now(tz=timezone.utc) + timedelta(seconds=expires_sec),
                'iat': datetime.now(tz=timezone.utc),
                'sub': sub
            }
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )

        except Exception as e:
            return e 
    
    def encode_access_token(self, user_id):
        expires_sec = 15 # 900 | 15 min
        access_token = self.encode_token(user_id, expires_sec)
        return access_token        

    def encode_refresh_token(self, new_auth):
        expires_sec = 60 # 86400 | one day
        refresh_token = self.encode_token(new_auth, expires_sec)
        return refresh_token

    def decode_access_token(self, access_token):
        try:
            payload = jwt.decode(
                access_token,
                SECRET_KEY,
                algorithms='HS256'
            )
            return payload
        except jwt.ExpiredSignatureError:
            message_error = 'Signature expired. Please log in again.'
            return message_error
        except jwt.InvalidTokenError:
            message_error = 'Invalid token. Please log in again.'
            return message_error

    def decode_refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(
                refresh_token,
                SECRET_KEY,
                algorithms='HS256'
            )
            user_id = payload['sub']
            new_auth_access = self.auth(user_id)
            return new_auth_access
        except jwt.ExpiredSignatureError:
            message_error = 'Signature expired. Please log in again.'
            return message_error
        except jwt.InvalidTokenError:
            message_error = 'Invalid token. Please log in again.'
            return message_error
from itsdangerous import URLSafeTimedSerializer
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
SECURE_SERIALIZER = URLSafeTimedSerializer(SECRET_KEY)

def create_secure_url(data: dict, expires_sec=3600):
    return SECURE_SERIALIZER.dumps(data)

def verify_secure_url(token: str, max_age=3600):
    return SECURE_SERIALIZER.loads(token, max_age=max_age)

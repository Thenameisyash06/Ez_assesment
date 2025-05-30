# from datetime import datetime, timedelta
# from jose import jwt

# SECRET_KEY = "your_jwt_secret_key"
# ALGORITHM = "HS256"
# EXPIRATION_MINUTES = 30

# def create_token(data: dict):
#     to_encode = data.copy()
#     to_encode.update({"exp": datetime.time() + timedelta(minutes=EXPIRATION_MINUTES)})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

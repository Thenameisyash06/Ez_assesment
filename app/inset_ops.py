import hashlib
import asyncio
from databases import users_collection

async def insert_ops_user():
    email = "yashd9404@gmail.com"
    password = "dubeyyash@06"

    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    existing_user = await users_collection.find_one({"email": email})
    if existing_user:
        print("Ops user already exists.")
        return

    await users_collection.insert_one({
        "email": email,
        "password": hashed_pw,
        "role": "ops"
    })

    print("Ops user inserted successfully.")

asyncio.run(insert_ops_user())

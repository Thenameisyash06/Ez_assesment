from fastapi import APIRouter, HTTPException
from app.models import ClientUser
from app.utils import secure_url
from app.databases import users_collection, files_collection
from bson import ObjectId
from fastapi import Header, Depends
from app.utils import jwt_handler
import hashlib
from fastapi.responses import FileResponse

router = APIRouter()

@router.post("/signup")
async def signup(user: ClientUser):
    hashed_pw = hashlib.sha256(user.password.encode()).hexdigest()

    if await users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=409, detail="Email already registered")

    result = await users_collection.insert_one({
        "email": user.email,
        "password": hashed_pw,
        "full_name": user.full_name,
        "verified": False,
        "role": "client"
    })

    token = secure_url.create_secure_url({"user_id": str(result.inserted_id)})
    verify_url = f"http://localhost:8000/client/verify-email?token={token}"

    print(f"[EMAIL SIMULATION] Verification URL: {verify_url}")
    return {"message": "Verification email sent", "verification_url": verify_url}


@router.get("/verify-email")
async def verify_email(token: str):
    try:
        data = secure_url.verify_secure_url(token)
        user_id = data["user_id"]
        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"verified": True}}
        )
        return {"message": "Email verified successfully"}
    except:
        raise HTTPException(status_code=400, detail="Invalid or expired token")


@router.post("/login")
async def login(user: ClientUser):
    hashed_pw = hashlib.sha256(user.password.encode()).hexdigest()
    existing_user = await users_collection.find_one({
        "email": user.email,
        "password": hashed_pw,
        "role": "client"
    })

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt_handler.create_access_token({"user_id": str(existing_user["_id"]), "role": "client"})

    if not existing_user.get("verified", False):
        raise HTTPException(status_code=403, detail="Email not verified")

    return {
        "message": "Login successful",
        # "user_id": str(existing_user["_id"]),
        "access_token": token,
        "token_type": "bearer"
    }

def get_current_client_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    
    token = authorization.split(" ")[1]
    decoded = jwt_handler.verify_token(token)

    if not decoded or decoded.get("role") != "client":
        raise HTTPException(status_code=403, detail="Unauthorized or expired token")
    
    return decoded

@router.get("/files")
async def list_files(current_user: dict = Depends(get_current_client_user)):
    files = await files_collection.find().to_list(100)
    return [{"id": str(f["_id"]), "filename": f["filename"], "filetype": f["filetype"]} for f in files]


@router.get("/download-file/{file_id}")
async def request_download(file_id: str):
    token = secure_url.create_secure_url({"file_id": file_id, "role": "client"})
    return {"download-link": f"/client/secure-download/{token}", "message": "success"}


@router.get("/secure-download/{token}")
async def secure_download(token: str):
    try:
        data = secure_url.verify_secure_url(token)
        if data.get("role") != "client":
            raise HTTPException(status_code=403, detail="Access denied")

        file_id = data["file_id"]
        file_data = await files_collection.find_one({"_id": ObjectId(file_id)})

        if not file_data:
            raise HTTPException(status_code=404, detail="File not found")

        file_path = f"uploaded_files/{file_data['filename']}"
        return FileResponse(path=file_path, filename=file_data["filename"])
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

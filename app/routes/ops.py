from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models import OpsUser
from fastapi import Header, Depends
from app.utils import jwt_handler
from app.databases import users_collection, files_collection
import hashlib
import os

router = APIRouter()

@router.post("/login")
async def login(user: OpsUser):
    hashed_pw = hashlib.sha256(user.password.encode()).hexdigest()
    existing_user = await users_collection.find_one({
        "email": user.email,
        "password": hashed_pw,
        "role": "ops"
    })

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt_handler.create_access_token({"user_id": str(existing_user["_id"]), "role": "ops"})

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }

def get_current_ops_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    
    token = authorization.split(" ")[1]
    decoded = jwt_handler.verify_token(token)

    if not decoded or decoded.get("role") != "ops":
        raise HTTPException(status_code=403, detail="Unauthorized or expired token")
    
    return decoded

@router.post("/upload-file")
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_ops_user)
):
    ext = file.filename.split(".")[-1]
    if ext not in ["pptx", "docx", "xlsx"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    os.makedirs("uploaded_files", exist_ok=True)
    file_path = f"uploaded_files/{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    metadata = {
        "filename": file.filename,
        "filetype": ext,
        "uploader": current_user["user_id"]
    }
    await files_collection.insert_one(metadata)

    return {"message": "File uploaded successfully"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import client, ops

app = FastAPI(
    title="Secure File Sharing System",
    description="REST API for secure file sharing between Ops and Client users.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(client.router, prefix="/client", tags=["Client"])
app.include_router(ops.router, prefix="/ops", tags=["Ops"])

@app.get("/")
def root():
    return {"message": "Welcome to the Secure File Sharing API"}

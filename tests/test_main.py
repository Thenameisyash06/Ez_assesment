import pytest
from httpx import AsyncClient, ASGITransport
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

@pytest.fixture(scope="module")
def async_client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_ops_login_success(async_client):
    response = await async_client.post("/ops/login", json={
        "email": "yashd9404@gmail.com",
        "password": "dubeyyash@06"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_file_upload_missing_token(async_client):
    files = {'file': ('test.docx', b'test data')}
    response = await async_client.post("/ops/upload-file", files=files)
    assert response.status_code == 422 

@pytest.mark.asyncio
async def test_client_access_files_without_login(async_client):
    response = await async_client.get("/client/files") 
    assert response.status_code == 422
   

from httpx import AsyncClient


async def test_create_user(ac: AsyncClient):
    response = await ac.post("/signup", json={
        "user_id": "rimma",
        "password": "rimma",
    })
    assert response.status_code == 200

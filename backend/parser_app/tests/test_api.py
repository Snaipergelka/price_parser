import pytest
from httpx import AsyncClient

from backend.parser_app.endpoint import app


@pytest.mark.anyio
async def test_create_user():
    async with AsyncClient(app=app, base_url="https://127.0.0.1:8000/user") as ac:
        response = await ac.post("/registration", json={"name": "string", "phone_number": "string"})
    assert response.status_code == 200
    assert response.json() == {"name": "string", "phone_number": "string"}


@pytest.mark.anyio
async def test_subscribe_to_product():
    async with AsyncClient(app=app, base_url="https://127.0.0.1:8000/subscription") as ac:
        response = await ac.post("/subscribe_to_product",
                                 json={"phone_number": "string",
                                 "url": "https://sephora.ru/make-up/lips/pomade/clarins-joli-rouge-gubnaya-prod1yvc/#store_263774"})
    assert response.status_code == 200
    assert response.json() == "Success"


@pytest.mark.anyio
async def test_show_all_subscribed_products_without_details():
    async with AsyncClient(app=app, base_url="https://127.0.0.1:8000/subscription") as ac:
        response = await ac.post("/all_subscribed_products_without_details",
                                 json={"phone_number": "string"})
    assert response.status_code == 200
    assert response.json() == [72]


@pytest.mark.anyio
async def test_show_all_subscribed_products_with_details():
    async with AsyncClient(app=app, base_url="https://127.0.0.1:8000/subscription") as ac:
        response = await ac.post("/all_subscribed_products_with_details",
                                 json={"phone_number": "string"})
    assert response.status_code == 200
    assert response.json()[0]["name"] == 'Clarins Joli Rouge Губная помада 263774' and \
           response.json()[0]["id"] == 72 and response.json()[0]["price_with_card"] == 2750 and \
           response.json()[0]["price_on_sale"] == 2750 and \
           response.json()[0]["product_id"] == 72


@pytest.mark.anyio
async def test_unsubscribe_product():
    async with AsyncClient(app=app, base_url="https://127.0.0.1:8000/subscription") as ac:
        response = await ac.post("/unsubscribe_product",
                                 json={"product_id": 72, "user_id": 69})
    assert response.status_code == 200
    assert response.json() == "Success"


@pytest.mark.anyio
async def test_delete_user():
    async with AsyncClient(app=app, base_url="https://127.0.0.1:8000/user") as ac:
        response = await ac.delete("/delete_user",
                                   params={"user_id": 69})
    assert response.status_code == 200
    assert response.json() == "Success"

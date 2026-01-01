# import packages
from fastapi import FastAPI
import httpx
from httpx import ASGITransport
from pymongo import AsyncMongoClient
import pytest
from testcontainers.mongodb import MongoDbContainer

# import code
from FI_API.main import get_app
from FI_API.internal.config import api_host
from FI_API.internal.hmdb import get_database, set_database



## ##-----------------------
@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def mongo_container():
    with MongoDbContainer("mongo:8.2") as mongo:
        yield mongo

@pytest.fixture()
async def test_client(mongo_container):
    # Test-Mongo starten
    mongo_url = mongo_container.get_connection_url()

    # AsyncMongoClient
    test_client = AsyncMongoClient(mongo_url)

    # Client in App überschreiben
    set_database(client=test_client)

    # FastAPI app
    app: FastAPI = get_app()

    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url=f"http://{api_host}") as ac:
        yield ac
    
    # End
    await test_client.close()


## start: & "C:/Users/teres/Documents/Code/HomeManager/Food Inventory/HM-Food-Inventory/.venv/Scripts/python.exe" -m pytest testing/ -v --tb=short

# import packages
from fastapi import FastAPI
import httpx
from pymongo import AsyncMongoClient
import pytest
from testcontainers.monbodb import MongoDbContainer

# import code
from FI_API.main import get_app
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
    with MongoDbContainer("mongo:7.0") as mongo:
        yield mongo

@pytest.fixture(scope="session")
async def test_client(mongo_container):
    # Test-Mongo starten
    mongo_url = mongo_container.get_connection_url()

    # AsyncMongoClient
    test_client = AsyncMongoClient(mongo_url)

    # Client in App überschreiben
    set_database(client=test_client)

    # FastAPI app
    app: FastAPI = get_app()

    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    # End
    await test_client.close()


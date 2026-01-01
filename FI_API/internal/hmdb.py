# import packages
from fastapi import HTTPException
import logging
from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure

# import code
from FI_API.internal.config import mongodb_port, mongodb_url, mongodb_pw, mongodb_user, db_name


## Database Operations ## -------------------------------------

hmdb_client = None
logger = logging.getLogger()

# connect database
async def connect_database():
    global hmdb_client
    connect_url = f"mongodb://{mongodb_user}:{mongodb_pw}@{mongodb_url}:{mongodb_port}"
    hmdb_client = AsyncMongoClient(connect_url)
    try:
        await hmdb_client.admin.command('ping')
        logger.info("Connected to MongoDB successfully.")
    except ConnectionFailure:
        logger.error(f"Failed to connect to MongoDB")
        raise HTTPException(status_code=500, detail="Fehler beim Verbindungsaufbau mit der Datenbank.")

# get database
def get_database():
    if not hmdb_client:
        raise HTTPException(status_code=500, detail="Fehler beim Verbindungsaufbau mit der Datenbank.")
    fidb = hmdb_client[db_name]
    return fidb

# disconnect database
def close_database():
    hmdb_client.close()
    logger.info("Disconnected from MongoDB.")

# set database for testing purposes
def set_database(client: AsyncMongoClient):
    global hmdb_client
    hmdb_client = client

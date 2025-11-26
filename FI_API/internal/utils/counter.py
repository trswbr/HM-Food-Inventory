# import packages


# import code
from internal.config import counter_collection_name, grocery_collection_name, \
    recipe_collection_name


## Counter Util ## --------------------------------------

from pymongo import AsyncMongoClient


async def _get_next_id(conn: AsyncMongoClient, collection: str):
    response = await conn[counter_collection_name].find_one_and_update(
        {"_id": collection},
        {"$inc": {"counter": 1}},
        upsert=True,
        return_document=True
    )
    return response["counter"]



async def get_grocery_id(conn: AsyncMongoClient):
    counter = await _get_next_id(collection=grocery_collection_name, conn=conn)
    return f"LM{counter:06d}"

async def get_recipe_id(conn: AsyncMongoClient):
    counter = await _get_next_id(collection=recipe_collection_name, conn=conn)
    return f"RE{counter:06d}"


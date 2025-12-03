# import packages
from fastapi import HTTPException
from pymongo import AsyncMongoClient
from typing import Union

# import code
from internal.config import db_name, grocery_collection_name, item_collection_name

# import models
from models.grocery_models import GetGrocery
from models.item_models import GetItem


## Utils ## ----------------------------------------------------
async def get_data_by_id(
        conn: AsyncMongoClient,
        collection_key: str,
        filter_id: Union[str, int]
) -> GetGrocery | GetItem:
    """
    Function to retrieve single document from specified collection.
    To prevent circular imports in CRUD when needing to get data from different collections.
    """
    col_type_dict = {
        "grocery": {
            "collection": grocery_collection_name,
            "return_type": GetGrocery
        },
        "item": {
            "collection": item_collection_name,
            "return_type": GetItem
        }
    }

    response = await conn[db_name][col_type_dict[collection_key]["collection"]].find_one({"_id": filter_id})
    if not response:
        raise HTTPException(status_code=404, detail=f"{collection_key.capitalize()} wurde nicht gefunden.") 
    
    return col_type_dict[collection_key]["return_type"](**response)


# import packages
from pymongo import AsyncMongoClient

# import code
from internal.config import db_name, grocery_collection_name

# import models
from models.grocery_models import Grocery


## Grocery Operations ## ------------------------------------------

async def crud_get_all_groceries(
        conn: AsyncMongoClient,
        filter: dict
) -> list[Grocery]:
    """
    Retrieve all groceries from the database based on the provided filter.
    
    :param conn: AsyncMongoClient - Database connection
    :param filter: dict - Filter criteria for querying groceries

    :return: list[Grocery] - List of groceries matching the filter
    """
    response_grocery = conn[db_name][grocery_collection_name].find(filter=filter)
    
    grocery_list = []
    for grocery in await response_grocery.to_list(length=None):
        grocery_list.append(Grocery(**grocery))
    
    return grocery_list


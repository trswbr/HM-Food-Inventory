# import packages
from pymongo import AsyncMongoClient

# import code
from internal.config import db_name, item_collection_name
from crud.grocery_operations import crud_get_all_groceries

# import models
from models.item_models import GetItemGrocery, ItemList


## Item Operations ## ------------------------------------------------

async def crud_get_all_items(
        conn: AsyncMongoClient,
        skip: int,
        limit: int,
        f_location: list = [],
        f_item_status: list = [],
        f_grocery_id: list = [],
        sort: list = ["grocery_id", 1]
) -> ItemList:
    """
    Retrieve all items from the database with optional filtering and pagination.

    :param conn: AsyncMongoClient - Database connection
    :param skip: int - Number of items to skip for pagination
    :param limit: int - Maximum number of items to return
    :param f_location: list - Filter by item locations
    :param f_item_status: list - Filter by item statuses
    :param f_grocery_id: list - Filter by grocery IDs
    :param sort: list - Sorting criteria and order

    :return: ItemList - List of items with grocery details
    """
    # Prepare filter query
    filter_query = {}
    
    for key, filter in {
        "location": f_location, 
        "item_status": f_item_status, 
        "grocery_id": f_grocery_id
        }:
        if filter:
            filter_query[key] = {"$in": filter}

    # Find items
    cursor_item = conn[db_name][item_collection_name].find(filter=filter_query, skip=skip, limit=limit).sort(*sort)
    response_items = await cursor_item.to_list()

    # Find corresponding groceries
    grocery_ids = [item["grocery_id"] for item in response_items]
    grocery_ids = list(set(grocery_ids))
    response_groceries = await crud_get_all_groceries(conn=conn, filter={"_id": {"$in": grocery_ids}})

    # Combine item and grocery data
    full_item_list = []
    for item in response_items:
        for grocery in response_groceries:
            if item["grocery_id"] == grocery.id:
                full_item_list.append(GetItemGrocery(**item, **grocery.model_dump(exclude={"id"})))

    return ItemList(count=len(full_item_list), limit=limit, skip=skip, items=full_item_list)


    
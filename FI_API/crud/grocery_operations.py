# import packages
from fastapi import HTTPException
from pymongo import AsyncMongoClient, ReturnDocument

# import code
from FI_API.internal.config import grocery_collection_name, item_collection_name
from FI_API.internal.utils.counter import get_grocery_id

# import models
from FI_API.models.grocery_models import GetGrocery, GetGroceryItems, GroceryList, CreateGrocery, Grocery, UpdateGrocery



## Grocery Operations ## ------------------------------------------

async def crud_get_all_groceries(
        conn: AsyncMongoClient,
        skip: int,
        limit: int,
        filter: dict
) -> GroceryList:
    """
    Retrieve all groceries from the database based on the provided filter.
    
    :param conn: AsyncMongoClient - Database connection
    :param filter: dict - Filter criteria for querying groceries

    :return: list[Grocery] - List of groceries matching the filter
    """
    response_grocery = conn[grocery_collection_name].find(filter=filter, limit=limit, skip=skip).sort("_id", 1)
    
    grocery_list = []
    for grocery in await response_grocery.to_list(length=None):
        grocery_list.append(Grocery(**grocery))
    
    return GroceryList(total_count=len(grocery_list), skip=skip, limit=limit, data=grocery_list)


async def crud_get_grocery(
        conn: AsyncMongoClient,
        grocery_id: str
) -> GetGrocery | None:
    """
    Retrieve a single grocery from the database by its ID.

    :param conn: AsyncMongoClient - Database connection
    :param grocery_id: str - Unique identifier of the grocery

    :return: GetGrocery | None - Grocery object if found, else None
    """

    response_grocery = await conn[grocery_collection_name].find_one(
        filter={"_id": grocery_id}
    )
    
    if response_grocery:
        return Grocery(**response_grocery)
    return None

async def crud_get_grocery_w_items(
        conn: AsyncMongoClient,
        grocery_id: str
) -> GetGroceryItems:
    """
    Retrieve a single grocery with related items.

    :param conn: AsyncMongoClient - Database connection
    :param grocery_id: str - Unique identifier of the grocery

    :return: GetGroceryItems - The requested grocery with related items
    """
    grocery = await crud_get_grocery(conn=conn, grocery_id=grocery_id)
    if not grocery:
        raise HTTPException(status_code=404, detail="Lebensmittel wurde nicht gefunden.")
    
    response_items = conn[item_collection_name].find({"grocery_id": grocery_id}).sort("best_before_date", 1)
    item_list = await response_items.to_list()

    return GetGroceryItems(**grocery.model_dump(), items=item_list)
    

async def crud_create_grocery(
        conn: AsyncMongoClient,
        grocery_data: CreateGrocery
) -> str:
    """
    Create a single grocery.

    :param conn: AsyncMongoClient - Database connection
    :param grocery_data: CreateGrocery - data of the grocery to be saved

    :return: str - ID of the grocery that was created
    """
    grocery_id = await get_grocery_id(conn=conn)

    response = await conn[grocery_collection_name].insert_one(Grocery(
        _id=grocery_id,
        **grocery_data.model_dump()
    ).model_dump(by_alias=True))

    return grocery_id


async def crud_update_grocery(
        conn: AsyncMongoClient,
        grocery_data: UpdateGrocery,
        grocery_id: str
) -> GetGrocery:
    """
    Updates a single grocery.

    :param conn: AsyncMongoClient - Database connection
    :param grocery_data: UpdateGrocery - data of the grocery to be updated
    :param grocery_id: str - ID of the grocery that gets updated
    """
    response = await conn[grocery_collection_name].find_one_and_update(
        filter={"_id": grocery_id},
        update={"$set": grocery_data.model_dump()},
        return_document=ReturnDocument.AFTER
    )

    if not response:
        raise HTTPException(status_code=404, detail="Lebensmittel wurde nicht gefunden.")
    return GetGrocery(**response)

async def crud_delete_all_groceries(
        conn: AsyncMongoClient
):
    """
    Deletes all groceries from the database. 

    :param conn: AsyncMongoClient - Database connection
    """
    await conn[grocery_collection_name].delete_many({})

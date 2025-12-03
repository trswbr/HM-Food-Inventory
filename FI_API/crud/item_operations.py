# import packages
from fastapi import HTTPException
from pymongo import AsyncMongoClient, ReturnDocument

# import code
from internal.config import db_name, item_collection_name
from internal.utils.counter import get_item_id
from internal.utils.utils import get_data_by_id

# import models
from models.item_models import GetItem, CreateItem, Item, GetItemGrocery, UpdateItem
from models.custom_models import ItemStatus



## Item Operations ## ------------------------------------------------
async def crud_get_all_items(
        conn: AsyncMongoClient,
        skip: int,
        limit: int,
        f_location: list = [],
        f_item_status: list = [],
        f_grocery_id: list = [],
        sort: list = ["grocery_id", 1]
) -> list[GetItem]:
    """
    Retrieve all items from the database with optional filtering and pagination.

    :param conn: AsyncMongoClient - Database connection
    :param skip: int - Number of items to skip for pagination
    :param limit: int - Maximum number of items to return
    :param f_location: list - Filter by item locations
    :param f_item_status: list - Filter by item statuses
    :param f_grocery_id: list - Filter by grocery IDs
    :param sort: list - Sorting criteria and order

    :return: list - List of items
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
    
    all_items = []
    async for item in cursor_item:
        all_items.append(GetItem(**item))

    return all_items


async def crud_get_item(
        conn: AsyncMongoClient,
        item_id: int
) -> GetItem | None:
    """
    Retrieve a single item from the database by its ID.

    :param conn: AsyncMongoClient - Database connection
    :param item_id: int - ID of the item to retrieve

    :return: GetItem - The requested item if found
    """
    response_item = await conn[db_name][item_collection_name].find_one({"_id": item_id})
    
    if response_item:
        return GetItem(**response_item)    
    return None


async def crud_get_item_w_grocery(
        conn: AsyncMongoClient,
        item_id: int
) -> GetItemGrocery:
    """
    Retrieve a single item along with its grocery details from the database by its ID.

    :param conn: AsyncMongoClient - Database connection
    :param item_id: int - ID of the item to retrieve

    :return: GetItemGrocery - The requested item with grocery details
    """
    item = await crud_get_item(conn, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Artikel wurde nicht gefunden.")


    grocery_data = await get_data_by_id(conn=conn, collection_key="grocery", filter_id=item.grocery_id)
    return GetItemGrocery(**item.model_dump(by_alias=True), **grocery_data.model_dump(exclude={"id"}))


async def crud_create_item(
        conn: AsyncMongoClient,
        item_data: CreateItem,
        grocery_id: str
) -> int:
    """
    Create a single item of a grocery.

    :param conn: AsyncMongoClient - Database connection
    :param item_data: CreateItem - data of the item to be saved
    :param grocery_id: str - ID of the grocery the item is related to

    :return: int - ID of the item that was created
    """
    item_id = await get_item_id(conn)
    
    response = await conn[db_name][item_collection_name].insert_one(Item(
        _id=item_id,
        grocery_id=grocery_id,
        **item_data.model_dump()
    ).model_dump(by_alias=True))

    return item_id


async def crud_update_item(
        conn: AsyncMongoClient,
        item_data: UpdateItem,
        item_id: int
) -> GetItem:
    """
    Updates a single item of grocery.

    :param conn: AsyncMongoClient - Database connection
    :param item_data: UpdateItem - data of the item to be updated
    :param item_id: int - ID of the item that gets updated

    :return: GetItem - newly updated item
    """
    response = await conn[db_name][item_collection_name].find_one_and_update(
        filter={"_id": item_id},
        update={"$set": item_data.model_dump()},
        return_document=ReturnDocument.AFTER
    )

    if not response:
        raise HTTPException(status_code=404, detail="Artikel wurde nicht gefunden.")
    return GetItem(**response)


async def _update_status_item(
        conn: AsyncMongoClient,
        item_id: int,
        new_status: ItemStatus
):
    """
    Updates the state of an item.

    :param conn: AsyncMongoClient - Database connection
    :param item_id: int - ID of the item to be updated
    :param new_status: ItemStatus - new state of item
    """
    response = await conn[db_name][item_collection_name].update_one(
        filter={"_id": item_id},
        update={"$set": {"item_status": new_status}}
    )

    if response.matched_count == 0:
        raise HTTPException(status_code=404, detail="Artikel wurde nicht gefunden.")

async def crud_item_status_opened(
        conn: AsyncMongoClient,
        item_id: int
):
    """
    Updates item status to 'opened'.
    """
    await _update_status_item(conn=conn, item_id=item_id, new_status=ItemStatus.opened)

async def crud_item_status_consumed(
        conn: AsyncMongoClient,
        item_id: int
):
    """
    Updates item status to 'consumed'.
    """
    await _update_status_item(conn=conn, item_id=item_id, new_status=ItemStatus.consumed)

async def crud_item_status_expired(
        conn: AsyncMongoClient,
        item_id: int
):
    """
    Updates item status to 'expired'.
    """
    await _update_status_item(conn=conn, item_id=item_id, new_status=ItemStatus.expired)

async def crud_item_status_disposed(
        conn: AsyncMongoClient,
        item_id: int
):
    """
    Updates item status to 'disposed'.
    """
    await _update_status_item(conn=conn, item_id=item_id, new_status=ItemStatus.disposed)


# TODO: Delete items - under 2 conditions: status=consumed/expired/disposed && report is done
## report logic not implemented yet ##

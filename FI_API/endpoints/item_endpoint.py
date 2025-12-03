# import packages
from fastapi import APIRouter, Depends
from fastapi.params import Query
from pymongo import AsyncMongoClient

# import code
from internal.hmdb import get_database
from crud.item_operations import crud_get_item_w_grocery, crud_create_item, crud_update_item, \
    crud_item_status_opened, crud_item_status_consumed, crud_item_status_disposed

# import models
from models.item_models import GetItemGrocery, CreateItem, UpdateItem, GetItem



## item endpoints ## --------------------------------------
router = APIRouter(
    prefix="/items",
    tags=["Artikel"]
)


@router.get("/show/{item_id}")
async def get_item(
    item_id: int,
    db: AsyncMongoClient = Depends(get_database)
) -> GetItemGrocery:
    return await crud_get_item_w_grocery(conn=db, item_id=item_id)


@router.post("/create")
async def create_item(
    item_data: CreateItem,
    grocery_id: str,
    db: AsyncMongoClient = Depends(get_database)
) -> int:
    return await crud_create_item(conn=db, item_data=item_data, grocery_id=grocery_id)


@router.put("/update")
async def update_item(
    item_data: UpdateItem,
    item_id: int,
    db: AsyncMongoClient = Depends(get_database)
) -> GetItem:
    return await crud_update_item(conn=db, item_data=item_data, item_id=item_id)


@router.put("/update/{item_id}/opened")
async def update_item_status_opened(
    item_id: int,
    db: AsyncMongoClient = Depends(get_database)
) -> None:
    return await crud_item_status_opened(conn=db, item_id=item_id)

@router.put("/update/{item_id}/consumed")
async def update_item_status_opened(
    item_id: int,
    db: AsyncMongoClient = Depends(get_database)
) -> None:
    return await crud_item_status_consumed(conn=db, item_id=item_id)

@router.put("/update/{item_id}/disposed")
async def update_item_status_opened(
    item_id: int,
    db: AsyncMongoClient = Depends(get_database)
) -> None:
    return await crud_item_status_disposed(conn=db, item_id=item_id)

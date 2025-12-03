# import packages
from fastapi import APIRouter, Depends
from fastapi.params import Query
from pymongo import AsyncMongoClient

# import code
from internal.hmdb import get_database
from crud.grocery_operations import crud_get_all_groceries, crud_get_grocery_w_items, \
    crud_create_grocery, crud_update_grocery

# import models
from models.grocery_models import GroceryList, GetGroceryItems, CreateGrocery, UpdateGrocery, \
    GetGrocery

## grocery endpoints ## --------------------------------------
router = APIRouter(
    prefix="/groceries",
    tags=["Lebensmittel"]
)

@router.get("/all")
async def get_all_groceries(
    skip: int = Query(default=0, description="Anzahl der zu überspringenden Lebensmittel."),
    limit: int = Query(default=10, description="Maximale Anzahl der zurückzugebenden Lebensmittel."),
    db: AsyncMongoClient = Depends(get_database)
) -> GroceryList:
    # TODO: Add filtering options
    return await crud_get_all_groceries(conn=db, skip=skip, limit=limit, filter={})

@router.get("/show/{grocery_id}")
async def get_grocery(
    grocery_id: str,
    db: AsyncMongoClient = Depends(get_database)
) -> GetGroceryItems:
    return await crud_get_grocery_w_items(conn=db, grocery_id=grocery_id)

@router.post("/create")
async def create_grocery(
    grocery_data: CreateGrocery,
    db: AsyncMongoClient = Depends(get_database)
) -> str:
    return await crud_create_grocery(conn=db, grocery_data=grocery_data)

@router.put("/update")
async def update_grocery(
    grocery_id: str,
    grocery_data: UpdateGrocery,
    db: AsyncMongoClient = Depends(get_database)
) -> GetGrocery:
    return await crud_update_grocery(conn=db, grocery_data=grocery_data, grocery_id=grocery_id)


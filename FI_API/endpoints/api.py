# import packages
from fastapi import APIRouter

# import code
from endpoints.grocery_endpoint import router as grocery_router
from endpoints.item_endpoint import router as item_router

api_router = APIRouter()
api_router.include_router(grocery_router)
api_router.include_router(item_router)

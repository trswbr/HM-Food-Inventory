# import packages
from fastapi import APIRouter

# import code
from FI_API.endpoints.grocery_endpoint import router as grocery_router

api_router = APIRouter()
api_router.include_router(grocery_router)

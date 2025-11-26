# import packages
from fastapi import APIRouter

# import code
from endpoints.article_endpoints import router as article_router

api_router = APIRouter()
api_router.include_router(article_router)

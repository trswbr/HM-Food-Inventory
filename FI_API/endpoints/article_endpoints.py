# import packages
from fastapi import APIRouter



## article endpoints ## --------------------------------------
router = APIRouter(
    prefix="/articles",
    tags=["Lebensmittel"]
)

@router.get("/all")
async def get_all_articles():
    return {"message": "Placeholder"}


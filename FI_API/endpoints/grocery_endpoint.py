# import packages
from fastapi import APIRouter



## article endpoints ## --------------------------------------
router = APIRouter(
    prefix="/groceries",
    tags=["Lebensmittel"]
)

@router.get("/all")
async def get_all_groceries():
    return {"message": "Placeholder"}


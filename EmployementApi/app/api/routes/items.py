from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Data model for POST request


class Item(BaseModel):
    name: str
    price: float

# GET endpoint


@router.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "description": "Sample item"}

# POST endpoint


@router.post("/items")
def create_item(item: Item):
    return {"message": "Item received", "data": item}

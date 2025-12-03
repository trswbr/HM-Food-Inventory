# import packages
import pytest


## Tests ## ---------------------------------------

## /groceries/create
# successfull
@pytest.mark.asyncio
async def test_create_grocery_successfull(test_client):
    payload = {
        "title": "Ja! Vollmilch 3.5%",
        "ingredient_group": "Milch",
        "category": "Vegane/Milchprodukte",
        "measurement": 1.0,
        "unit": "l",
        "receipt_names": {
            "REWE": ["JA! VOLLMLCH 3.5%"]
        }
    }
    response = await test_client.post("/groceries/create", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert "_id" in data

    response_get = await test_client.get(f"/groceries/show/{data["_id"]}")
    db_data = response_get.json()
    assert db_data["title"] == payload["title"]
    assert db_data["measurement"] == payload["measurement"]


# optional fields are optional
required_test_fields = {"title": "X", "ingredient_group": "Y", "category": "Fleisch"}
@pytest.mark.parametrize("payload", [
    {**required_test_fields, "measurement": 1.0, "unit": "g"}, # missing receipt_names
    {**required_test_fields, "measurement": 1.0, "receipt_names": {"A": ["B"]}}, # missing unit; TODO: bind measurement & unit, if one is present require the other
    {**required_test_fields, "unit": "g", "receipt_names": {"A": ["B"]}}
])
@pytest.mark.asyncio
async def test_create_nullable_fields(test_client, payload):
    response = await test_client.post("/grocery/create", json=payload)
    assert response.status_code == 201

# error when: missing required fields, invalid enum, invalid type
@pytest.mark.parametrize("payload", [
    {"ingredient_group": "Milch", "category": "Vegane/Milchprodukte"}, # title is missing
    {"title": "Ja! Vollmilch", "ingredient_group": "Milch"}, # category is missing
    {"title": "Ja! Vollmilch", "category": "Vegane/Milchprodukte"}, # ingredient_group is missing
    {"title": "Ja! Vollmilch", "ingredient_group": "Milch", "category": "Milch"}, # wrong enum for category
    {"title": 21, "ingredient_group": "Milch", "category": "Vegane/Milchprodukte"} # wrong data type for title
])
@pytest.mark.asyncio
async def test_create_wrong_model_data(test_client, payload):
    response = await test_client.post("/grocery/create", json=payload)
    assert response.status_code == 422
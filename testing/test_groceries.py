# import packages
import pytest


## Tests ## ---------------------------------------
test_data = {
    "title": "Ja! Vollmilch 3.5%",
    "ingredient_group": "Milch",
    "category": "Vegane/Milchprodukte",
    "measurement": 1.0,
    "unit": "l",
    "receipt_names": {
        "REWE": ["JA! VOLLMLCH 3.5%"]
    }
}
url_prefix = "/groceries"
url_get_all = url_prefix + "/all"
url_show = url_prefix + "/show"
url_create = url_prefix + "/create"
url_update = url_prefix + "/update"
url_reset = url_prefix + "/reset"

## /groceries/create
# successfull
@pytest.mark.asyncio
async def test_create_grocery_successfull(test_client):
    payload = test_data
    response = await test_client.post(url_create, json=payload)

    assert response.status_code == 200
    data = response.json()

    response_get = await test_client.get(f"{url_show}/{data}")
    db_data = response_get.json()
    assert "_id" in db_data


# optional fields are optional
required_test_fields = {"title": "X", "ingredient_group": "Y", "category": "Fleisch"}
@pytest.mark.parametrize("payload", [
    {**required_test_fields, "measurement": 1.0, "unit": "g"}, # missing receipt_names
    {**required_test_fields, "measurement": 1.0, "receipt_names": {"A": ["B"]}}, # missing unit; TODO: bind measurement & unit, if one is present require the other
    {**required_test_fields, "unit": "g", "receipt_names": {"A": ["B"]}}
])
@pytest.mark.asyncio
async def test_create_nullable_fields(test_client, payload):
    response = await test_client.post(url_create, json=payload)
    assert response.status_code == 200


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
    response = await test_client.post(url_create, json=payload)
    assert response.status_code == 422


## /groceries/update
# successfull
@pytest.mark.asyncio
async def test_update_grocery_successfull(test_client):
    payload = test_data.copy()
    response = await test_client.post(url_create, json=payload)
    assert response.status_code == 200

    grocery_id = response.json()
    payload["title"] = "Ja! Fettarme Milch 1.5%"
    payload["receipt_names"]["REWE"] = ["JA! FETTARME MLK 1.5%"]
    response_update = await test_client.put(f"{url_update}?grocery_id={grocery_id}", json=payload)
    assert response_update.status_code == 200

    updated_data = response_update.json()
    assert updated_data["title"] != test_data["title"]
    assert updated_data["receipt_names"]["REWE"][0] == payload["receipt_names"]["REWE"][0]


## /groceries/all
# successfull
@pytest.mark.asyncio
async def test_get_all_groceries_successfull(test_client):
    response = await test_client.delete(url_reset)
    response_get = await test_client.get(url_get_all)
    data0 = response_get.json()
    assert data0["total_count"] == 0

    payload = test_data.copy()
    i = 0
    while i < 15:
        response = await test_client.post(url_create, json=payload)
        i += 1
    assert response.status_code == 200

    response_get1 = await test_client.get(url_get_all)
    assert response_get1.status_code == 200
    data1 = response_get1.json()
    assert data1["total_count"] == 10

    response_get2 = await test_client.get(f"{url_get_all}?skip=10")
    assert response_get2.status_code == 200
    data2 = response_get2.json()
    assert data2["total_count"] == 5

    response_get3 = await test_client.get(f"{url_get_all}?limit=20")
    assert response_get3.status_code == 200
    data3 = response_get3.json()
    assert data3["total_count"] == 15

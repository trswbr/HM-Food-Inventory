# import packages
from typing import Optional
from pydantic import Field

# import code
from models.custom_models import CustomBase, Category, ResponseListBase, UnitType


## Grocery Models ## ----------------------------------------------------------------
class GroceryBase(CustomBase):
    title: str = Field(
        title="Lebensmittelname",
        description="Genaue Bezeichnung des Lebensmittels"
    )
    ingredient_group: str = Field(
        title="Zutatengruppe",
        description="Gruppe der Zutat, dem dieses Lebensmittel zugeordnet ist"
    )
    category: Category = Field(
        title="Kategorie",
        description="Kategorie des Lebensmittels"
    )
    measurement: Optional[float] = Field(
        title="Mengenangabe",
        desccription="Angabe der Menge pro Stück"
    )
    unit: Optional[UnitType] = Field(
        title="Maßeinheit",
        description="Einheit der Mengenangabe"
    )
    receipt_names: Optional[dict[str, list[str]]] = Field(
        title="Kassenzettelbezeichnung",
        description="Bezeichnungen, die auf dem Kassenzettel für dieses Lebensmittel erscheinen"
    )

class Grocery(GroceryBase):
    id: str = Field(
        title="Lebensmittel ID",
        description="Eindeutige Kennung des Lebensmittels",
        alias="_id"
    )


class GetGrocery(Grocery):
    pass

class GetGroceryItems(GetGrocery):
    items: list = Field(
        title="Artikel Liste",
        description="Liste der zugehörigen Artikel"
    )

class CreateGrocery(GroceryBase):
    pass

class UpdateGrocery(GroceryBase):
    pass


class GroceryList(ResponseListBase):
    data: list[Grocery] = Field(
        title="Lebensmittel Liste",
        description="Liste der Lebensmittel"
    )


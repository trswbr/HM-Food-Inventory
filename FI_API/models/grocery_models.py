# import packages
from pydantic import Field, Optional

# import code
from models.custom_models import CustomBase, Category, UnitType
from models.item_models import Item


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
    receipt_names: Optional[dict[str, str]] = Field(
        title="Kassenzettelbezeichnung",
        description="Bezeichnungen, die auf dem Kassenzettel für dieses Lebensmittel erscheinen"
    )

class Grocery(GroceryBase):
    id: str = Field(
        title="Lebensmittel ID",
        description="Eindeutige Kennung des Lebensmittels",
        alias="_id"
    )
    items: Optional[list[Item]] = Field(default=[],
        title="Artikel",
        description="Liste der Artikel, die zu diesem Lebensmittel gehören"
    )


class GetGrocery(Grocery):
    pass

class CreateGrocery(GroceryBase):
    pass

class UpdateGrocery(GroceryBase):
    pass

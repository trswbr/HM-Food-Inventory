# import packages
from enum import Enum
from pydantic import BaseModel, Field


## -----------------------------------------------------------

class CustomBase(BaseModel):
    model_config = {
        "populate_by_name": True
    }


class ResponseListBase(CustomBase):
    count: int = Field()
    limit: int = Field()
    skip: int = Field()


class Carbs(CustomBase):
    total: float = Field(
        title="Kohlenhydrate insgesamt",
        description="Gesamtkohlenhydrate in Gramm"
    )
    sugar: float = Field(
        title="Zucker",
        description="Zuckergehalt in Gramm"
    )
    fiber: float = Field(
        title="Ballaststoffe",
        description="Ballaststoffgehalt in Gramm"
    )

class Nutrients(CustomBase):
    calories: float = Field(
        title="Kalorien",
        description="Energiegehalt in Kilokalorien"
    )
    protein: float = Field(
        title="Protein",
        description="Eiweißgehalt in Gramm"
    )
    carbs: Carbs = Field(
        title="Kohlenhydrate",
        description="Kohlenhydratgehalt in Gramm"
    )
    fats: float = Field(
        title="Fett",
        description="Fettgehalt in Gramm"
    )
    other: dict[str, float] = Field(
        title="Weitere Nährstoffe",
        description="Weitere Nährstoffangaben in Gramm"
    )


# Enums
class Locations(str, Enum):
    kitchen = "Küche"
    k_fridge = "Kühlschrank (Küche)"
    k_freezer = "Gefrierschrank (Küche)"
    g_fridge = "Kühlschrank (Garage)"
    g_freezer = "Gefrierschrank (Garage)"
    pantry = "Hauswirtschaftsraum"
    other = "Sonstiges"

class Category(str, Enum):
    fruits = "Obst"
    vegetables = "Gemüse"
    grains = "Teigwaren & Reis"
    dairy = "Vegane/Milchprodukte"
    meat = "Fleisch"
    fish = "Fisch & Meeresfrüchte"
    eggs = "Eier"
    snacks = "Snacks & Süßigkeiten"
    condiments = "Gewürze & Soßen"
    frozen = "Tiefkühlprodukte"
    convenience = "Fertiggerichte"
    leftovers = "Reste"
    other = "Sonstiges"

class ItemStatus(str, Enum):
    available = "vorhanden"
    opened = "angebrochen"
    consumed = "verbraucht"
    expired = "abgelaufen"
    discarded = "entsorgt"

class UnitType(str, Enum):
    grams = "g"
    kilograms = "kg"
    milliliters = "ml"
    liters = "l"
    pieces = "Stück"
    packs = "Packung"
    bottles = "Flasche"
    cans = "Dose"
    tablespoons = "EL"
    teaspoons = "TL"
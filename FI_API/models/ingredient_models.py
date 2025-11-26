# import packages
from enum import Enum
from pydantic import Field, Optional



## Ingredient Models ## ----------------------------------------------------------------
class Locations(str, Enum):
    K_fridge = "Küche - Kühlschrank"
    K_freezer = "Küche - Gefrierschrank"
    G_fridge = "Garage - Kühlschrank"
    G_freezer = "Garage - Gefrierschrank"
    pantry = "Vorratsschrank"
    other = "Sonstiges"

class ArticleBase():
    name: str = Field(
        title="Zutatenbezeichnung"
    )
    quantity: Optional[float] = Field(default=1.0,
        title="Stückzahl"
    )
    measurement: Optional[int] = Field(
        title="Mengenangabe",
        desccription="Angabe der Menge pro Stück"
    )
    unit: Optional[str] = Field(
        title="Maßeinheit",
        description="Einheit der Mengenangabe"
    )
    location: Locations = Field(
        title="Lagerort"
    )

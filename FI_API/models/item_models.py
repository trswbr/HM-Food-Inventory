# import packages
from datetime import datetime, timedelta
from pydantic import Field, Optional

# import code
from models.custom_models import CustomBase, Locations, ItemStatus


## Item Models ## ----------------------------------------------------------
class ItemBase(CustomBase):
    location: Locations = Field(
        title="Lagerort"
    )
    item_status: ItemStatus = Field(
        title="Status des Lebensmittels"
    )
    note: Optional[str] = Field(
        title="Anmerkung",
        description="Beliebige Anmerkungen zum Artikel"
    )
    
class Item(ItemBase):
    id: int = Field(
        title="Artikel ID",
        description="Eindeutige Kennung des Artikels",
        alias="_id"
    )
    grocery_id: str = Field(
        title="Lebensmittel ID",
        description="Eindeutige Kennung des zugehörigen Lebensmittels"
    )
    best_before_date: datetime = Field(
        title="Mindesthaltbarkeitsdatum",
        description="Mindesthaltbarkeitsdatum des Lebensmittels"
    )
    purchase_date: datetime = Field(
        title="Kaufdatum",
        description="Datum, an dem das Lebensmittel gekauft wurde"
    )
    price: Optional[float] = Field(
        title="Preis",
        description="Preis des Lebensmittels in Euro"
    )



class GetItem(Item):
    pass

class CreateItem(ItemBase):
    best_before_date: Optional[datetime] = Field(default=datetime.now()+timedelta(days=10),
        title="Mindesthaltbarkeitsdatum",
        description="Mindesthaltbarkeitsdatum des Lebensmittels"
    )
    purchase_date: Optional[datetime] = Field(default=datetime.now(),
        title="Kaufdatum",
        description="Datum, an dem das Lebensmittel gekauft wurde"
    )

class UpdateItem(ItemBase):
    pass

class DeleteItem(Item):
    pass

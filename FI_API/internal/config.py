# import packages
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()
load_dotenv(".env")

# get environment variables
## API
api_host = os.getenv("API_HOST", None)
api_port = os.getenv("API_PORT", None)

## MongoDB
mongodb_user = os.getenv("MONGODB_USER", "")
mongodb_pw = os.getenv("MONGODB_PW", "")
mongodb_url = os.getenv("MONGODB_URL", "localhost")
mongodb_port = os.getenv("MONGODB_PORT", "27017")

db_name = "food_inventory"
grocery_collection_name = "Lebensmittel"
item_collection_name = "Artikel"
recipe_collection_name = "Rezepte"

counter_collection_name = "ID Counter"





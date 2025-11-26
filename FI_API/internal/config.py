# import packages
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()
load_dotenv(".env")

# get environment variables
## API
api_host = os.getenv("API_HOST")
api_port = os.getenv("API_PORT")

## MongoDB
mongodb_user = os.getenv("MONGODB_USER")
mongodb_pw = os.getenv("MONGODB_PW")
mongodb_url = os.getenv("MONGODB_URL")
mongodb_port = os.getenv("MONGODB_PORT")

db_name = "food_inventory"
article_collection_name = "Lebensmittel"
recipe_collection_name = "Rezepte"







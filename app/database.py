
from motor.motor_asyncio import AsyncIOMotorClient

# CONFIGURATION ACTUELLE (NE PAS TOUCHER)
MONGO_URL = "mongodb+srv://new-user:1E10A8TVeqycmo4m@cluster0.9qj2las.mongodb.net/?appName=Cluster0"

# Initialisation
client = AsyncIOMotorClient(MONGO_URL)
db = client.cv_builder_database 

# Collections
cvs_collection = db.get_collection("cvs")
users_collection = db.get_collection("users")
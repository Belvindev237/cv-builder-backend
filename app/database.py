
from motor.motor_asyncio import AsyncIOMotorClient

# CONFIGURATION ACTUELLE (NE PAS TOUCHER)
MONGO_URL = "mongodb+srv://new-user:1E10A8TVeqycmo4m@cluster0.9qj2las.mongodb.net/?appName=Cluster0"
MONGO_URI="mongodb://localhost:27017/cv_builder"

# Initialisation
client = AsyncIOMotorClient(MONGO_URL)
db = client.cv_builder_database 

# Collections
cvs_collection = db.get_collection("cvs")
users_collection = db.get_collection("users")
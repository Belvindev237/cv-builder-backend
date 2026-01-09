from motor.motor_asyncio import AsyncIOMotorClient

# L'adresse locale de ton MongoDB
MONGO_URL = "mongodb+srv://new-user:1E10A8TVeqycmo4m@cluster0.9qj2las.mongodb.net/?appName=Cluster0"

# Création du client et choix du nom de la base de données
client = AsyncIOMotorClient(MONGO_URL)
db = client.cv_builder_database  # Tu peux changer ce nom si tu veux
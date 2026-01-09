from fastapi import FastAPI
from app.database import db  # On importe la connexion depuis ton fichier database.py
from app.routes import auth  # On importe le routeur d'authentification
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mon API avec FastAPI et MongoDB")
app.include_router(auth.router)  # On inclut le routeur d'authentification
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
async def create_test_user():
    # On définit un utilisateur de test
    #user_test = {"name": "Doros", "email": "test@mail.com"}
    
    # On l'insère dans une collection appelée "users"
    # C'est cette ligne qui va créer la base et la collection !
    #result = await db.users.insert_one(user_test)
    
    return {"message": "Bienvenue sur mon API FastAPI avec MongoDB!"}

@app.get("/")
def read_root():
     return {"message": "Bienvenue sur mon API FastAPI avec MongoDB!"}
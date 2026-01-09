from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

# 1. Configuration du hachage
# On utilise bcrypt qui est le standard de l'industrie
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Configuration du Token JWT (pour plus tard)
SECRET_KEY = "TA_CLE_TRES_SECRETE_NE_PAS_PARTAGER" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# --- Fonction pour hacher le mot de passe ---
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# --- Fonction pour vérifier le mot de passe lors du login ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# --- Fonction pour créer le badge d'accès (JWT) ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
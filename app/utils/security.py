from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.database import db
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
# 1. Configuration du hachage
# On utilise bcrypt qui est le standard de l'industrie
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Configuration du Token JWT (pour plus tard)
SECRET_KEY = "TA_CLE_TRES_SECRETE_NE_PAS_PARTAGER" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES =60

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # 1. On nettoie le token au cas où
        token = token.replace("Bearer ", "")
        
        # 2. On tente le décodage avec la clé forcée en string
        payload = jwt.decode(
            token, 
            str(SECRET_KEY), 
            algorithms=[ALGORITHM]
        )
        
        print(f"SUCCÈS ! Payload : {payload}")
        return payload.get("sub")

    except JWTError as e:
        # CE PRINT EST LE PLUS IMPORTANT MAINTENANT
        print(f"ÉCHEC DÉCODAGE. Raison : {str(e)}")
        # Si ça affiche "Signature verification failed", c'est la SECRET_KEY qui est différente du login
        raise HTTPException(status_code=401, detail="Could not validate credentials")


from fastapi import APIRouter, HTTPException, status
from app.models.cv_model import CVModel
from app.database import cvs_collection,db
from datetime import datetime
from bson import ObjectId
from app.utils.security import get_current_user
from fastapi import Depends
from app.models import users


router = APIRouter(prefix="/cv", tags=["operation_cv"])

@router.post("/create_cv", status_code=status.HTTP_201_CREATED)
async def create_cv(cv_data: CVModel,current_user:users=Depends(get_current_user)):
    try:
        # 1. Conversion du modèle en dictionnaire
        new_cv = cv_data.model_dump()
        
        # 2. Ajout de la date (Correction du nom created_at au lieu de created_id pour plus de clarté)
        new_cv["created_at"] = datetime.now()
        new_cv["user_id"]=current_user
        
        # 3. Insertion dans MongoDB
        result = await cvs_collection.insert_one(new_cv)
        
        return {
            "message": "Cv enregistré avec succès",
            "id": str(result.inserted_id)
        }
        
    except Exception as e:
        # Affiche l'erreur réelle dans ton terminal pour débugger
        print(f"Détail de l'erreur MongoDB : {str(e)}")
        
        # CORRECTION : l'argument est status_code, pas status
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur survenue lors de l'enregistrement : {str(e)}"
        )


# ... tes autres imports et ton router ...




@router.get("/user_cvs")
async def get_user_cvs(current_user: str = Depends(get_current_user)):
    print(current_user)
    try:
        # On utilise ton nom de variable spécifique
       
        cursor = cvs_collection.find({"user_id": current_user})
        cvs = await cursor.to_list(length=100)
        
        # Transformation pour le frontend (ObjectId -> String)
        for cv in cvs:
            cv["id"] = str(cv["_id"])
            del cv["_id"]
            
        return cvs
    except Exception as e:
        print(f"Erreur Dashboard : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des CV")
    
    
@router.get("/{cv_id}")
async def get_cv(cv_id: str):
    try:
        # 1. Vérifier si l'ID fourni est un format ObjectId valide
        if not ObjectId.is_valid(cv_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Format d'ID invalide"
            )

        # 2. Chercher le CV dans la collection
        cv = await cvs_collection.find_one({"_id": ObjectId(cv_id)})

        # 3. Si le CV n'existe pas
        if cv is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="CV non trouvé dans la base de données"
            )

        # 4. Convertir l'ObjectId de MongoDB en string pour le JSON
        cv["_id"] = str(cv["_id"])
        
        # Si tu as un champ 'created_at' de type datetime, 
        # assure-toi qu'il est aussi converti si nécessaire (FastAPI le gère souvent seul)

        return cv

    except Exception as e:
        print(f"Erreur lors de la récupération : {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )
    

@router.put("/{cv_id}")
async def update_cv(cv_id:str, update_data:dict ,current_user:str = Depends(get_current_user)):
    if not ObjectId.is_valid(cv_id):
        raise HTTPException(status_code=404, detail="format ID invalide")
    existing_cv=cvs_collection.find_one({"_id":ObjectId(cv_id),"user_id":current_user})
    if not existing_cv:
        raise HTTPException(status_code=404 , detail="Cv non trouvé ou acces refusé")
    result= await cvs_collection.update_one(
        {"_id":ObjectId(cv_id)},
        {"$set":update_data}
    )
    if result.modified_count==0:
        return {"message": "Aucune modification effectuée"}
    return {"message":"Cv modifié avec succès!"}
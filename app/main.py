import asyncio
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
from playwright.sync_api import sync_playwright  # ✅ Version synchrone
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from app.database import db  # On importe la connexion depuis ton fichier database.py
from app.routes import auth  # On importe le routeur d'authentification
from app.routes import cv_route
from fastapi.middleware.cors import CORSMiddleware
import json
from pydantic import BaseModel
from fastapi.responses import Response

app = FastAPI(title="Mon API avec FastAPI et MongoDB")
app.include_router(auth.router)  # On inclut le routeur d'authentification
app.include_router(cv_route.router)
origins = [
    "https://cv-builder-iota-three.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
]

# 2. Applique la configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # <--- UTILISE LA LISTE, PAS "*"
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



class PDFRequest(BaseModel):
    html: str
    fileName: str = "cv.pdf"

def generate_pdf_sync(html: str):
    print("🔄 Démarrage de la génération PDF...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("📄 Chargement du HTML...")
        page.set_content(html, wait_until='domcontentloaded')
        
        print("⏳ Attente (2 secondes)...")
        page.wait_for_timeout(2000)
        
        text_content = page.evaluate("document.body.innerText")
        print(f"📝 Contenu texte: {len(text_content)} caractères")
        
        if len(text_content) < 50:
            print("⚠️ Attention: Peu de contenu détecté!")
        
        print("🖨️ Génération du PDF...")
        pdf_bytes = page.pdf(
            format='A4',
            print_background=True,
            margin={'top': '0mm', 'right': '0mm', 'bottom': '0mm', 'left': '0mm'}
        )
        
        print(f"✅ PDF généré: {len(pdf_bytes)} octets")
        browser.close()
        
        return pdf_bytes

executor = ThreadPoolExecutor(max_workers=2)

@app.post("/generate-pdf")
async def generate_pdf(request: PDFRequest):
    try:
        loop = asyncio.get_event_loop()
        pdf_bytes = await loop.run_in_executor(
            executor, 
            generate_pdf_sync, 
            request.html
        )
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={request.fileName}",
                "Content-Length": str(len(pdf_bytes))
            }
        )
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

@app.get("/")
def root():
    return {"message": "API PDF Generator", "status": "running"}

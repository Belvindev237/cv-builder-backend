# On utilise l'image officielle Playwright qui contient déjà Linux + Python + Dépendances Navigateur
FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy

# Définir le dossier de travail
WORKDIR /app

# Copier le fichier de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Installer Chromium (les dépendances système sont déjà là, donc pas d'erreur de mot de passe !)
RUN playwright install chromium

# Copier tout le reste du code
COPY . .

# Commande pour lancer ton serveur FastAPI / Uvicorn
# Note : Render utilise le port 10000 par défaut
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
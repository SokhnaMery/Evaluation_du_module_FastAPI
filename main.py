from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import csv
import random
from typing import List  # Importer List depuis typing

app = FastAPI()
security = HTTPBasic()

# Définition des utilisateurs avec leurs mots de passe
users_db = {
    "username": ["alice", "bob", "clementine", "admin"],
    "password": ["wonderland", "builder", "mandarine", "4dm1N"]
}

# Modèle pour les données de question
class Question(BaseModel):
    question: str
    subject: str
    use: str
    
# Modèle pour les données de création de question
class CreateQuestion(BaseModel):
    question: str
    subject: str
    use: str
    correct: str
    responseA: str
    responseB: str
    responseC: str
    responseD: str = None

# Fonction pour charger les questions depuis le fichier CSV
def load_questions_from_csv(file_path: str):
    try:
        with open(file_path, newline='') as csvfile:
            lecteur = csv.DictReader(csvfile)
            questions = list(lecteur)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Impossible de trouver le fichier CSV")
    return questions

# Chargement des questions depuis le fichier CSV
questions = load_questions_from_csv('questions.csv')

# Fonction pour vérifier les identifiants
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username in users_db["username"] and credentials.password in users_db["password"]:
        return credentials.username
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/")
async def read_root():
    return {"message": "Welcome to my FastAPI application!"}

# Point de terminaison pour récupérer des questions aléatoires
@app.get("/questions/")
def get_questions(
    use: str = Query(...),
    subjects: List[str] = Query(...),
    question_count: int = Query(...),
    user: str = Depends(authenticate_user)
):
    filtered_questions = [q for q in questions if q['use'] == use and q['subject'] in subjects]
    
    print(f"Nombre de questions filtrées: {len(filtered_questions)}")
    
    if len(filtered_questions) < question_count:
        selected_questions = filtered_questions  # Renvoie toutes les questions disponibles si moins que question_count
    else:
        selected_questions = random.sample(filtered_questions, question_count)
    
    # Écrire les questions sélectionnées dans un fichier CSV
    with open('selected_questions.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=questions[0].keys())
        writer.writeheader()
        writer.writerows(selected_questions)

    return {"questions": selected_questions}

# Point de terminaison pour créer une nouvelle question (réservé aux administrateurs)
@app.post("/questions/")
def create_question(question: CreateQuestion, user: str = Depends(authenticate_user)):
    if user != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create questions")
    
    # Ajouter la nouvelle question à la liste en mémoire
    questions.append(question.dict())
    
    # Enregistrer la nouvelle question dans un nouveau fichier CSV
    with open('new_questions.csv', mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=question.dict().keys())
        if file.tell() == 0:
            writer.writeheader()  # Écrire l'en-tête seulement si le fichier est vide
        writer.writerow(question.dict())
    
    return {"message": "Question created successfully"}

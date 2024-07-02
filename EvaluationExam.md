Vous trouverez ci-après un fichier zip contenant la structure de rendu de l'examen. Attention, il n'est pas autorisé de modifier les noms de fichiers ou d'en ajouter.

wget https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/fastapi_exam_XXXX.zip
Dézippez ce dossier compressé et vous pouvez commencer à coder directement dans les fichiers mis à disposition.

Les données
Notre base de données est représentée par un fichier csv présent dans l'archive de l'examen ci-dessous.

On y retrouve les champs suivants:

question: l'intitulé de la question
subject: la catégorie de la question
correct: la liste des réponses correctes
use: le type de QCM pour lequel cette question est utilisée
responseA: réponse A
responseB: réponse B
responseC: réponse C
responseD: la réponse D (si elle existe)
Explorez ce jeu de données pour comprendre ces données.

L'API
Sur l'application ou le navigateur Web, l'utilisateur doit pouvoir choisir un type de test (use) ainsi qu'une ou plusieurs catégories (subject). De plus, l'application peut produire des QCMs de 5, 10 ou 20 questions. L'API doit donc être en mesure de retourner ce nombre de questions. Comme l'application doit pouvoir générer de nombreux QCMs, les questions doivent être retournées dans un ordre aléatoire: ainsi, une requête avec les mêmes paramètres pourra retourner des questions différentes.

⚠ Attention. Dans le fichier main.py, il est obligatoire d'appeler la variable qui contiendra l'instance FastAPI(): app .
Authentification
L'API utilise une authentification basique, à base de nom d'utilisateur et de mot de passe. Les informations d'authentification doivent être incluses dans les en-têtes (headers) de la requête. Le nom d'utilisateur et le mot de passe doivent être envoyés encodés en Base64 dans le format suivant : Authorization: Basic <credentials>, où <credentials> est la chaîne Base64 de la forme username:password.

Pour les identifiants, on pourra utiliser le dictionnaire suivant:

{
  "alice": "wonderland",
  "bob": "builder",
  "clementine": "mandarine"
}
Endpoints
1. /verify
Description: Vérifie que l'API est fonctionnelle.
Méthode HTTP: GET
Exemple de réponse: {"message": "L'API est fonctionnelle."}
2. /generate_quiz
Description: Génère un QCM basé sur les paramètres fournis.
Méthode HTTP: POST
Payload:
"test_type": Le type de test souhaité (par exemple "multiple_choice").
"categories": Une liste des catégories de questions souhaitées.
"number_of_questions": Le nombre de questions à inclure dans le QCM.
Authentification:
Utilise l'authentification basique avec les en-têtes (headers) de la requête.
Réponse:
Une liste de questions au format JSON.
Exemple de requête:
    POST /generate_quiz HTTP/1.1
    Host: example.com
    Authorization: {‘username’: ‘test’, password: ‘test’} 
    Content-Type: application/json

    {
      "test_type": "multiple_choice",
      "categories": ["math", "history"],
      "number_of_questions": 10
    }
    
Exemple de réponse:
  [
    {
      "question": "Quelle est la capitale de la France ?",
      "subject": "geography",
      "correct": ["Paris"],
      "use": "multiple_choice",
      "responseA": "Londres",
      "responseB": "Paris",
      "responseC": "Berlin",
      "responseD": "Madrid"
    },
    {
      "question": "Qui a peint la Joconde ?",
      "subject": "art",
      "correct": ["Leonardo da Vinci"],
      "use": "multiple_choice",
      "responseA": "Picasso",
      "responseB": "Van Gogh",
      "responseC": "Leonardo da Vinci",
      "responseD": "Michel-Ange"
    },
    ...
  ]
  
Erreurs possibles:
Si l'authentification échoue, renvoyer un code d'erreur approprié avec un message explicatif.
Si les paramètres fournis sont incorrects ou si aucune question ne correspond aux critères, renvoyer un code d'erreur avec un message.
3. /create_question
Description: Crée une nouvelle question par un utilisateur admin.
Méthode HTTP: POST
Payload:
  {
    "admin_username": "admin",
    "admin_password": "4dm1N",
    "question": "Quelle est la capitale de la France ?",
    "subject": "geography",
    "correct": ["Paris"],
    "use": "multiple_choice",
    "responseA": "Londres",
    "responseB": "Paris",
    "responseC": "Berlin",
    "responseD": "Madrid"
  }
  
Exemple de réponse: {"message": "Question créée avec succès."}

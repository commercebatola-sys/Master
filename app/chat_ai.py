import os
from openai import OpenAI

# --- Configuration ------------------------------------------------------------------
# IMPORTANT : Ta clé API doit être définie comme variable d'environnement dans Render :
# RENDER → Environment → Add Variable → KEY = "OPENAI_API_KEY" ; VALUE = ta clé.
# -------------------------------------------------------------------------------------

# Récupération automatique de la clé API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY est introuvable. Ajoute-la dans les variables d'environnement Render.")

# Initialisation client OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)


# --- Fonction pour résumer un texte ---------------------------------------------------
def summarize_text(text: str, max_words: int = 250):
    """
    Résume le texte envoyé. max_words = limite maximale du résumé.
    """

    prompt = f"Résumé clair et structuré en moins de {max_words} mots : {text}"

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Tu es un expert en analyse de documents et résumé."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400
    )

    return response.choices[0].message.content


# --- Fonction Question/Réponse --------------------------------------------------------
def ask_question(document_text: str, user_question: str):
    """
    Répond à la question de l'utilisateur.
    Peut utiliser le document mais aussi ses propres connaissances si nécessaire.
    """

    prompt = f"Le document est : {document_text}\n\nQuestion : {user_question}. Réponds même si l'information n'est pas dans le document."

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Tu es un assistant intelligent capable d'expliquer, analyser et compléter le document avec tes connaissances."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    return response.choices[0].message.content


# --- Génération de questions suggérées -------------------------------------------------
def generate_suggested_questions(document_text: str):
    """
    Génère automatiquement 4 questions pertinentes basées sur le document.
    """

    prompt = (
        "Génère 4 questions intelligentes qu'un utilisateur poserait après avoir lu ce document. "
        "Pas de réponses, seulement les questions."
        f"\n\nDocument : {document_text}"
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Tu es un expert en analyse documentaire."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=180
    )

    return response.choices[0].message.content.split("\n")
  

# ml_models.py
import os
from openai import OpenAI

# ===============================
# 1 — Initialisation OpenAI
# ===============================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY est introuvable. Ajoute-la dans les variables d'environnement.")

client = OpenAI(api_key=OPENAI_API_KEY)


# ===============================
# 2 — Résumé automatique
# ===============================
def summarize_text(text: str, max_words: int = 250) -> str:
    """
    Résume un texte donné en un résumé structuré.
    max_words : limite approximative de mots.
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


# ===============================
# 3 — Question/Réponse
# ===============================
def ask_question(document_text: str, user_question: str) -> str:
    """
    Répond à une question posée par l'utilisateur.
    Peut utiliser le document mais aussi ses connaissances générales si nécessaire.
    """
    prompt = (
        f"Le document est : {document_text}\n\n"
        f"Question : {user_question}. Réponds même si l'information n'est pas dans le document."
    )

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "Tu es un assistant intelligent capable d'expliquer et d'analyser un document."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content


# ===============================
# 4 — Questions suggérées
# ===============================
def generate_suggested_questions(document_text: str) -> list:
    """
    Génère automatiquement 4 questions pertinentes basées sur le document.
    Retourne une liste de questions.
    """
    prompt = (
        "Génère 4 questions intelligentes qu'un utilisateur poserait après avoir lu ce document. "
        "Pas de réponses, seulement les questions.\n\n"
        f"Document : {document_text}"
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Tu es un expert en analyse documentaire."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=180
    )

    questions = response.choices[0].message.content.split("\n")
    # Nettoyage : retirer les lignes vides
    return [q.strip() for q in questions if q.strip()]

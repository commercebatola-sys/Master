import os
from openai import OpenAI
from supabase import create_client, Client
from dotenv import load_dotenv

# --- Chargement des variables d'environnement ---------------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY est introuvable.")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ Supabase URL ou Key manquante.")

# --- Initialisation clients ----------------------------------------------------------
client = OpenAI(api_key=OPENAI_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Fonctions existantes ------------------------------------------------------------
def summarize_text(text: str, max_words: int = 250):
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

def ask_question(document_text: str, user_question: str):
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

def generate_suggested_questions(document_text: str):
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

# --- Nouvelles fonctions pour Supabase -----------------------------------------------
def save_conversation(session_id: str, user_message: str, ai_response: str):
    """Enregistre une conversation dans Supabase"""
    try:
        supabase.table("conversations").insert({
            "session_id": session_id,
            "user_message": user_message,
            "ai_response": ai_response
        }).execute()
    except Exception as e:
        print(f"Impossible de sauvegarder la conversation : {e}")

def get_conversation_history(session_id: str):
    """Récupère tout l'historique pour une session"""
    try:
        data = supabase.table("conversations").select("*").eq("session_id", session_id).order("created_at").execute()
        return data.data if data.data else []
    except Exception as e:
        print(f"Impossible de récupérer l'historique : {e}")
        return []

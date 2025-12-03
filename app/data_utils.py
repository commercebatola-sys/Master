# data_utils.py
import os
from supabase import create_client, Client

# ----------------------------
# 1 — Connexion Supabase
# ----------------------------
SUPABASE_URL = "https://ezwsorvmbiuevykxfotc.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Assure-toi que la clé est dans l'environnement
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ----------------------------
# 2 — Fonctions utilitaires
# ----------------------------
def get_conversations():
    """
    Récupère toutes les conversations de la table 'conversations'
    """
    data = supabase.table("conversations").select("*").execute()
    return data.data if data.data else []


def add_summary(document_name: str, summary: str):
    """
    Ajoute un résumé pour un document
    """
    supabase.table("conversations").insert({
        "document_name": document_name,
        "summary": summary
    }).execute()


def add_question_answer(document_name: str, question: str, answer: str):
    """
    Ajoute une question et sa réponse pour un document
    """
    supabase.table("conversations").insert({
        "document_name": document_name,
        "summary": "",
        "question": question,
        "answer": answer
    }).execute()


def clear_conversations():
    """
    Supprime toutes les conversations (utile pour tests)
    """
    supabase.table("conversations").delete().neq("document_name", "").execute()

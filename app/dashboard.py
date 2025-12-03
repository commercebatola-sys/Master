# dashboard.py
import streamlit as st
from chat_ai import summarize_text, ask_question, generate_suggested_questions
from supabase import create_client, Client
import os

# ----------------------------
# 1 — Connexion à Supabase
# ----------------------------
SUPABASE_URL = "https://ezwsorvmbiuevykxfotc.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Ajoute ta clé Supabase dans l'environnement
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------------
# 2 — Interface Streamlit
# ----------------------------
st.title("📊 Dashboard Conversations")

# Onglets pour gérer l'affichage
tab1, tab2 = st.tabs(["📝 Historique", "💬 Nouvelle Analyse"])

with tab1:
    st.header("Historique des conversations")

    # Récupération des conversations depuis Supabase
    data = supabase.table("conversations").select("*").execute()
    conversations = data.data if data.data else []

    if conversations:
        for conv in conversations[::-1]:  # afficher du plus récent au plus ancien
            st.markdown(f"**Document :** {conv.get('document_name', 'Inconnu')}")
            st.markdown(f"**Résumé :**\n{conv.get('summary', '')}")
            if conv.get("question"):
                st.markdown(f"**Question :** {conv.get('question')}")
                st.markdown(f"**Réponse :** {conv.get('answer', '')}")
            st.markdown("---")
    else:
        st.info("Aucune conversation disponible pour le moment.")

with tab2:
    st.header("💬 Nouvelle Analyse de Document")
    
    uploaded_file = st.file_uploader("Choisissez un PDF", type=["pdf"])
    
    if uploaded_file:
        texte = uploaded_file.read().decode("latin1")  # ou utf-8 selon ton PDF
        st.success("✅ Document chargé")

        # Bouton pour générer un résumé
        if st.button("📄 Générer le résumé"):
            summary = summarize_text(texte, max_words=250)
            st.markdown("### Résumé généré :")
            st.markdown(summary)

            # Stocker la conversation dans Supabase
            supabase.table("conversations").insert({
                "document_name": uploaded_file.name,
                "summary": summary
            }).execute()
            st.success("✅ Résumé sauvegardé dans l'historique")

        # Section questions interactives
        question = st.text_input("Posez une question sur ce document")
        if question and st.button("❓ Obtenir la réponse"):
            answer = ask_question(texte, question)
            st.markdown("### Réponse :")
            st.markdown(answer)

            # Stocker question + réponse dans Supabase
            supabase.table("conversations").insert({
                "document_name": uploaded_file.name,
                "summary": "",
                "question": question,
                "answer": answer
            }).execute()
            st.success("✅ Question & réponse sauvegardées")

        # Suggestions automatiques
        if st.button("💡 Questions suggérées"):
            suggested = generate_suggested_questions(texte)
            st.markdown("### Questions suggérées :")
            for q in suggested:
                st.markdown(f"- {q}")

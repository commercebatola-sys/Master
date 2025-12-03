
# home.py
import streamlit as st
from pathlib import Path

# ===============================
# Page d'accueil
# ===============================
def show_home():
    st.set_page_config(
        page_title="Accueil - Analyse Financière",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🏠 Bienvenue sur l'Analyseur Financier Automatisé")
    st.markdown(
        """
        Transformez vos documents financiers en **résumés clairs**, **questions/réponses intelligentes**
        et suivez facilement l'historique de vos analyses.
        """
    )

    st.markdown("---")

    # -------------------------------
    # Sections principales
    # -------------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📄 Upload & Analyse")
        st.markdown(
            """
            - Téléversez vos PDF financiers.
            - Obtenez un résumé structuré automatiquement.
            - Posez des questions spécifiques sur le document.
            """
        )
        if st.button("➡️ Aller à Upload"):
            st.session_state["page"] = "upload"

    with col2:
        st.subheader("📊 Dashboard")
        st.markdown(
            """
            - Suivez toutes vos analyses passées.
            - Consultez les résumés et conversations enregistrées.
            - Filtrez et recherchez vos documents.
            """
        )
        if st.button("➡️ Aller au Dashboard"):
            st.session_state["page"] = "dashboard"

    with col3:
        st.subheader("💬 Chat IA")
        st.markdown(
            """
            - Posez des questions sur vos documents.
            - Obtenez des suggestions automatiques de questions.
            - Analyse intelligente même si l'info n'est pas dans le PDF.
            """
        )
        if st.button("➡️ Aller au Chat IA"):
            st.session_state["page"] = "chat_ai"

    st.markdown("---")

    # -------------------------------
    # Informations / Instructions
    # -------------------------------
    st.subheader("ℹ️ Instructions rapides")
    st.markdown(
        """
        1. Commencez par téléverser un document dans **Upload & Analyse**.
        2. Consultez vos analyses passées dans le **Dashboard**.
        3. Posez des questions ou explorez le document avec **Chat IA**.
        4. Tous les résumés et conversations sont enregistrés pour consultation future.
        """
    )

    st.markdown(
        "💡 **Astuce** : Vous pouvez télécharger les résumés en PDF ou Markdown, selon votre préférence."
    )

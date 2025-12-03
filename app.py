# app.py
import streamlit as st
from fpdf import FPDF
import tempfile
from app import upload, chat_ai, themes

# ===============================
# 0 — Appliquer thème
# ===============================
themes.apply_theme()  # Si tu as une fonction pour thème moderne

# ===============================
# 1 — Configuration page
# ===============================
st.set_page_config(
    page_title="Analyse Automatique de Documents Financiers",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Analyse Automatique de Documents Financiers")
st.markdown("Transformez vos PDF financiers en résumé clair et chiffré.")

# ===============================
# 2 — Upload PDF
# ===============================
uploaded_file = st.file_uploader("Choisissez un PDF", type=["pdf"])
if uploaded_file:
    try:
        texte = upload.extract_pdf_text(uploaded_file)  # Utilise ton module upload.py
    except Exception as e:
        st.error(f"❌ Erreur lors de l'extraction du PDF : {e}")
        st.stop()

    LONGUEUR_MAX = 250_000
    if len(texte) > LONGUEUR_MAX:
        texte = texte[:LONGUEUR_MAX]
        st.warning(f"⚠️ Le texte a été tronqué à {LONGUEUR_MAX} caractères")

    st.success("✅ PDF chargé et traité.")

    # Aperçu du texte
    with st.expander("👁️ Aperçu du texte extrait"):
        st.text(texte[:1000] + ("..." if len(texte) > 1000 else ""))

    # ===============================
    # 3 — Résumé automatique
    # ===============================
    st.subheader("🤖 Génération du résumé")
    with st.spinner("📊 Résumé en cours..."):
        try:
            resume = chat_ai.summarize_text(texte, max_words=250)
        except Exception as e:
            st.error(f"❌ Erreur lors de la génération du résumé : {e}")
            resume = None

    if resume:
        st.markdown("### 📊 Résumé généré :")
        st.markdown(resume)

        # Télécharger Markdown
        st.download_button(
            label="💾 Télécharger Markdown",
            data=resume,
            file_name=f"resume_{uploaded_file.name.replace('.pdf','')}.md",
            mime="text/markdown"
        )

        # Télécharger PDF
        pdf_temp = FPDF()
        pdf_temp.add_page()
        pdf_temp.set_auto_page_break(auto=True, margin=15)
        pdf_temp.set_font("Arial", size=12)
        for line in resume.split("\n"):
            pdf_temp.multi_cell(0, 5, line)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            pdf_temp.output(tmp_pdf.name)
            tmp_pdf.seek(0)
            pdf_data = tmp_pdf.read()
            st.download_button(
                label="💾 Télécharger PDF",
                data=pdf_data,
                file_name=f"resume_{uploaded_file.name.replace('.pdf','')}.pdf",
                mime="application/pdf"
            )

    # ===============================
    # 4 — Questions interactives
    # ===============================
    st.subheader("❓ Posez une question sur le PDF")
    question = st.text_input("Exemple : Quel est le chiffre d'affaires ?")

    # Génération de 4 questions suggérées automatiquement
    try:
        questions_suggerees = chat_ai.generate_suggested_questions(texte)
    except:
        questions_suggerees = [
            "Quel est le chiffre d'affaires ?",
            "Quelle est la marge nette ?",
            "Quels sont les principaux risques identifiés ?",
            "Quelle est la dette nette ?"
        ]

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Rechercher la réponse"):
            if question:
                with st.spinner("🤖 Recherche en cours..."):
                    try:
                        reponse_question = chat_ai.ask_question(texte, question)
                        st.markdown("### 💡 Réponse :")
                        st.markdown(reponse_question)
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la réponse : {e}")
    with col2:
        st.subheader("💡 Questions suggérées")
        for q in questions_suggerees:
            if st.button(q, key=q):
                with st.spinner("🤖 Recherche en cours..."):
                    try:
                        reponse_question = chat_ai.ask_question(texte, q)
                        st.markdown("### 💡 Réponse :")
                        st.markdown(reponse_question)
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la réponse : {e}")

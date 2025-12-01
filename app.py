# app.py
import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import pathlib
from fpdf import FPDF
import tempfile

# ===============================
# 1 — Chargement du .env
# ===============================
env_path = pathlib.Path(".env")
load_dotenv(dotenv_path=env_path)
default_api_key = os.getenv("OPENAI_API_KEY", "")

if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = default_api_key

# ===============================
# 2 — Interface Streamlit
# ===============================
st.set_page_config(
    page_title="Analyse Automatique de Documents Financiers",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Analyse Automatique de Documents Financiers")
st.markdown("Transformez vos PDF financiers en résumé clair et chiffré.")

# -------------------------------
# Clé API
# -------------------------------
api_key_input = st.text_input(
    "🔑 Clé API OpenAI",
    value=st.session_state.openai_api_key,
    type="password",
    placeholder="sk-..."
)
if api_key_input != st.session_state.openai_api_key:
    st.session_state.openai_api_key = api_key_input
    st.success("✅ Clé API mise à jour !")

if not st.session_state.openai_api_key:
    st.warning("❌ Entrez votre clé API pour continuer.")
    st.stop()

client = OpenAI(api_key=st.session_state.openai_api_key)

# -------------------------------
# Upload PDF
# -------------------------------
uploaded_file = st.file_uploader("Choisissez un PDF", type=["pdf"])
if uploaded_file:
    try:
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        texte = ""
        for i, page in enumerate(pdf, start=1):
            texte_page = page.get_text()
            texte += f"\n\n=== [PAGE {i}] ===\n{texte_page.strip()}"
        texte = "\n".join(l.strip() for l in texte.splitlines())
    except Exception as e:
        st.error(f"❌ Erreur lors de la lecture du PDF : {e}")
        st.stop()

    st.success("✅ PDF chargé et traité.")

    # -------------------------------
    # Longueur maximale
    # -------------------------------
    LONGUEUR_MAX = st.slider(
        "Longueur max du texte à analyser",
        min_value=50_000,
        max_value=200_000,
        value=120_000,
        step=10_000
    )
    if len(texte) > LONGUEUR_MAX:
        texte = texte[:LONGUEUR_MAX]
        st.warning(f"⚠️ Le texte a été tronqué à {LONGUEUR_MAX} caractères")

    # -------------------------------
    # Aperçu du texte
    # -------------------------------
    with st.expander("👁️ Aperçu du texte extrait"):
        st.text(texte[:1000] + ("..." if len(texte) > 1000 else ""))

    # -------------------------------
    # Consignes pour le résumé
    # -------------------------------
    consignes_resume = (
        "Tu es analyste financier. On te fournit le texte d'un document financier.\n"
        "Produis une synthèse précise et chiffrée en Markdown selon ce cadre :\n"
        "- Société / Période / Devise\n"
        "- Résumé exécutif (5–8 lignes)\n"
        "- Chiffres clés (tableau Markdown)\n"
        "- Analyse\n"
        "- Références internes\n"
        "N'invente aucun chiffre. Cite la page d'origine si possible."
    )

    modele = "gpt-4o-mini"
    with st.spinner("🤖 Génération du résumé en cours..."):
        try:
            reponse = client.responses.create(
                model=modele,
                input=[
                    {"role": "system", "content": consignes_resume},
                    {"role": "user", "content": texte},
                ],
            )
            resume = reponse.output_text
        except Exception as e:
            st.error(f"❌ Erreur lors de la génération du résumé : {e}")
            resume = None

    if resume:
        st.markdown("### 📊 Résumé généré :")
        st.markdown(resume)

        # -------------------------------
        # Téléchargement Markdown
        # -------------------------------
        st.download_button(
            label="💾 Télécharger Markdown",
            data=resume,
            file_name=f"resume_{uploaded_file.name.replace('.pdf','')}.md",
            mime="text/markdown"
        )

        # -------------------------------
        # Téléchargement PDF
        # -------------------------------
        pdf_temp = FPDF()
        pdf_temp.add_page()
        pdf_temp.set_auto_page_break(auto=True, margin=15)
        pdf_temp.set_font("Arial", size=12)
        for line in resume.split("\n"):
            pdf_temp.multi_cell(0, 5, line)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            pdf_temp.output(tmp_pdf.name)
            tmp_pdf.seek(0)
            st.download_button(
                "💾 Télécharger PDF",
                data=tmp_pdf,
                file_name=f"resume_{uploaded_file.name.replace('.pdf','')}.pdf"
            )

    # -------------------------------
    # Questions interactives
    # -------------------------------
    st.subheader("❓ Posez une question sur le PDF")
    question = st.text_input("Exemple : Quel est le chiffre d'affaires ?")
    questions_suggerees = [
        "Quel est le chiffre d'affaires ?",
        "Quelle est la marge nette ?",
        "Quels sont les principaux risques identifiés ?",
        "Quelle est la dette nette ?",
        "Quel est le cash flow opérationnel ?"
    ]

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Rechercher la réponse"):
            if question:
                consignes_question = (
                    "Tu es analyste financier. Réponds uniquement à la question posée, "
                    "sans inventer de données. Si la réponse n'est pas claire, écris 'non précisé'. "
                    "Indique la page d'origine si possible."
                )
                with st.spinner("🤖 Recherche en cours..."):
                    try:
                        reponse_question = client.responses.create(
                            model=modele,
                            input=[
                                {"role": "system", "content": consignes_question},
                                {"role": "user", "content": f"Question : {question}\n\nTexte PDF :\n{texte}"},
                            ],
                        )
                        st.markdown("### 💡 Réponse :")
                        st.markdown(reponse_question.output_text)
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la réponse à la question : {e}")
    with col2:
        st.subheader("💡 Questions suggérées")
        for q in questions_suggerees:
            if st.button(q, key=q):
                with st.spinner("🤖 Recherche en cours..."):
                    consignes_question = (
                        "Tu es analyste financier. Réponds uniquement à la question posée, "
                        "sans inventer de données. Si la réponse n'est pas claire, écris 'non précisé'. "
                        "Indique la page d'origine si possible."
                    )
                    try:
                        reponse_question = client.responses.create(
                            model=modele,
                            input=[
                                {"role": "system", "content": consignes_question},
                                {"role": "user", "content": f"Question : {q}\n\nTexte PDF :\n{texte}"},
                            ],
                        )
                        st.markdown("### 💡 Réponse :")
                        st.markdown(reponse_question.output_text)
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la réponse : {e}")

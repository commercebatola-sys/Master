# app.py
import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st
import pathlib

# ===============================
# 1 — Chargement du .env
# ===============================
env_path = pathlib.Path(".env")
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# ===============================
# 2 — Interface Streamlit
# ===============================
st.title("📊 Résumé Automatique de Documents Financiers")
st.markdown("Transformez vos PDF financiers en résumé clair et chiffré.")

uploaded_file = st.file_uploader("Choisissez un PDF", type=["pdf"])
if uploaded_file:
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    texte = ""
    for i, page in enumerate(pdf, start=1):
        texte_page = page.get_text()
        texte += f"\n\n=== [PAGE {i}] ===\n{texte_page.strip()}"
    texte = "\n".join(l.strip() for l in texte.splitlines())
    LONGUEUR_MAX = 120_000
    if len(texte) > LONGUEUR_MAX:
        texte = texte[:LONGUEUR_MAX]

    st.text("✅ PDF chargé et traité.")

    # ===============================
    # 3 — Consignes pour l'IA
    # ===============================
    consignes = (
        "Tu es analyste financier. On te fournit le texte d'un document financier.\n"
        "Produis une synthèse précise et chiffrée en Markdown selon ce cadre :\n"
        "- Société / Période / Devise\n"
        "- Résumé exécutif (5–8 lignes)\n"
        "- Chiffres clés (tableau Markdown)\n"
        "- Analyse\n"
        "- Références internes\n"
        "N'invente aucun chiffre. Cite la page d'origine si possible."
    )

    # ===============================
    # 4 — Appel API OpenAI
    # ===============================
    modele = "gpt-4o-mini"
    reponse = client.responses.create(
        model=modele,
        input=[
            {"role": "system", "content": consignes},
            {"role": "user", "content": texte},
        ],
    )

    resume = reponse.output_text

    # ===============================
    # 5 — Affichage Streamlit
    # ===============================
    st.markdown("### Résumé généré :")
    st.markdown(resume)

    # ===============================
    # 6 — Questions interactives
    # ===============================
    question = st.text_input("Posez une question sur le PDF")
    if question:
        consignes_questions = (
            "Tu es analyste financier. Réponds uniquement à la question posée, "
            "sans inventer de données. Si la réponse n'est pas claire, écris 'non précisé'. "
            "Indique la page d'origine si possible."
        )
        reponse_question = client.responses.create(
            model=modele,
            input=[
                {"role": "system", "content": consignes_questions},
                {"role": "user", "content": f"Question : {question}\n\nTexte PDF :\n{texte}"},
            ],
        )
        st.markdown("### Réponse :")
        st.markdown(reponse_question.output_text)

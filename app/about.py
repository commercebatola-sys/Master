
about.py

import streamlit as st

def show_about():
"""Affiche la page 'À propos' de l'application."""

st.title("ℹ️ À propos de l'application")

st.markdown(
    """
    **Nom de l'application :** Analyseur Financier Automatique  
    **Version :** 1.0.0  
    **Créateur :** BATOLA KISSADI Manace Dalvy Gates  
    **Objectif :** Transformez vos PDF financiers en résumés clairs et chiffrés, avec analyse des chiffres clés et possibilité de poser des questions spécifiques.  

    **Fonctionnalités principales :**
    - Analyse automatique de PDF financiers
    - Génération de résumés structurés
    - Questions interactives sur le document
    - Téléchargement en PDF ou Markdown
    - Historique des documents analysés

    **Contact / Support :** contact@alinyxe.com
    """
)

st.markdown("---")
st.info("Cette application utilise l'API OpenAI pour l'analyse et la génération des résumés financiers.")

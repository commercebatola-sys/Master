# themes.py

import streamlit as st

# ===============================
# 1 — Couleurs principales
# ===============================
PRIMARY_COLOR = "#1f77b4"   # Bleu principal
SECONDARY_COLOR = "#ff7f0e" # Orange secondaire
SUCCESS_COLOR = "#2ca02c"   # Vert succès
WARNING_COLOR = "#d62728"   # Rouge / Alerte
BACKGROUND_COLOR = "#f5f5f5"
TEXT_COLOR = "#111111"

# ===============================
# 2 — Styles CSS pour Streamlit
# ===============================
def apply_custom_theme():
    """
    Applique les styles CSS personnalisés à Streamlit.
    """
    st.markdown(
        f"""
        <style>
        /* Couleur du fond principal */
        .stApp {{
            background-color: {BACKGROUND_COLOR};
            color: {TEXT_COLOR};
        }}

        /* Titre principal */
        .stTitle {{
            color: {PRIMARY_COLOR};
            font-weight: 700;
        }}

        /* Boutons */
        div.stButton > button:first-child {{
            background-color: {PRIMARY_COLOR};
            color: white;
            border-radius: 8px;
            height: 40px;
        }}
        div.stButton > button:first-child:hover {{
            background-color: {SECONDARY_COLOR};
            color: white;
        }}

        /* Slider */
        .stSlider > div > div > div > div {{
            background-color: {PRIMARY_COLOR};
        }}

        /* TextInput / TextArea */
        input, textarea {{
            border: 1px solid {PRIMARY_COLOR};
            border-radius: 6px;
        }}

        /* Success / warning messages */
        .stSuccess {{ color: {SUCCESS_COLOR}; font-weight: 600; }}
        .stWarning {{ color: {WARNING_COLOR}; font-weight: 600; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ===============================
# 3 — Fonctions utilitaires
# ===============================
def set_page_config():
    """
    Configuration globale de la page Streamlit.
    """
    st.set_page_config(
        page_title="Analyse Financière IA",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def sidebar_header(title: str):
    """
    Affiche un titre dans la sidebar avec un style uniforme.
    """
    st.sidebar.markdown(f"### {title}")

def colored_markdown(text: str, color: str = PRIMARY_COLOR):
    """
    Affiche du texte markdown coloré.
    """
    st.markdown(f"<span style='color:{color}'>{text}</span>", unsafe_allow_html=True)

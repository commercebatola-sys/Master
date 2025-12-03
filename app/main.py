# main.py
import streamlit as st
from app import home, dashboard, chat_ai, about, advisors  # Import des modules du dossier app
# Si tu as d'autres pages comme upload.py ou data_utils.py, tu peux aussi les importer

# ===============================
# Initialisation de la session
# ===============================
if "page" not in st.session_state:
    st.session_state["page"] = "home"  # Page par défaut

# ===============================
# Barre latérale pour navigation
# ===============================
st.sidebar.title("Navigation")
menu_options = {
    "🏠 Accueil": "home",
    "📄 Upload & Analyse": "upload",
    "📊 Dashboard": "dashboard",
    "💬 Chat IA": "chat_ai",
    "👥 Advisors": "advisors",
    "ℹ️ About": "about"
}

# Sélection du menu
choice = st.sidebar.radio("Aller à :", list(menu_options.keys()))
st.session_state["page"] = menu_options[choice]

# ===============================
# Affichage des pages
# ===============================
def render_page(page_name):
    if page_name == "home":
        home.show_home()
    elif page_name == "upload":
        # Ici, si tu as un fichier upload.py avec une fonction show_upload()
        from app import upload
        upload.show_upload()
    elif page_name == "dashboard":
        dashboard.show_dashboard()
    elif page_name == "chat_ai":
        chat_ai.show_chat_ai()
    elif page_name == "advisors":
        advisors.show_advisors()
    elif page_name == "about":
        about.show_about()
    else:
        st.error("❌ Page non trouvée !")

render_page(st.session_state["page"])

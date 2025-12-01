
advisors.py

import streamlit as st

def show_advisors():
"""Affiche la page des conseillers / recommandations"""

st.title("💼 Conseillers et recommandations")

st.markdown(
    """
    Cette section fournit des conseils financiers généraux et des contacts de conseillers qualifiés.  
    **Important :** Les recommandations sont indicatives. Vérifiez toujours auprès d’un expert avant de prendre des décisions financières.
    """
)

st.subheader("Nos conseillers partenaires")
st.markdown("""
| Nom | Spécialité | Contact |
|-----|------------|---------|
| Jean Dupont | Analyse financière | jean.dupont@finance.com |
| Marie Leroy | Comptabilité & audit | marie.leroy@finance.com |
| Alain Ngoma | Stratégie d’entreprise | alain.ngoma@consulting.com |
""")

st.subheader("Recommandations générales")
st.markdown("""
- Toujours vérifier les chiffres avant toute décision
- Analyser les tendances sur plusieurs périodes
- Comparer avec les standards du marché
- Ne pas se baser uniquement sur les prévisions, diversifier les sources
""")

st.info("Cette page peut être mise à jour avec de nouveaux conseillers ou recommandations selon vos besoins.")

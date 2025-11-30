Alinyxe AI — Analyseur Financier (MASTER)

Version : "MASTER - Alinyxe"
But : Fournir une plateforme plug-and-play capable d’analyser des documents financiers (PDF) et des jeux de données (CSV / Excel), d’effectuer des prévisions simples, d’afficher un dashboard professionnel et d’offrir un chat IA contextuel — le tout prêt à l’usage pour les clients, sans qu’ils voient ni modifient la configuration technique.

---

Points clés — ce que fait l’application

- Analyse et résumé automatique de rapports financiers (PDF) avec IA.
- Extraction de tableaux et texte depuis les PDF.
- Upload multi-format : CSV, XLSX, PDF, JSON.
- Analyses prédictives simples (régression linéaire, forecasting basique).
- Dashboard interactif (KPIs, graphiques Plotly, filtres).
- Chat IA contextuel (multi-tours) avec historique (stocké localement ou côté serveur).
- Module de conseils automatiques (règles business + suggestions).
- Export des résultats (CSV / Markdown / téléchargement simple).
- Architecture MASTER → CLIENT : template maître verrouillé, duplication client personnalisée.

---

Sécurité & comportement plug-and-play

«Important : la clé API OpenAI (ou autre moteur IA) est intégrée côté serveur par l’équipe Alinyxe.
Les clients ne saisissent pas de clé API et n’ont pas accès aux paramètres techniques.
Aucune donnée sensible n’est exposée dans l’interface.»

---

Arborescence principale (version MASTER)

alinyxe_master/
├── app/
│   ├── __init__.py
│   ├── main.py            # point d'entrée (Streamlit)
│   ├── dashboard.py
│   ├── chat_ai.py
│   ├── ml_models.py
│   ├── data_utils.py
│   ├── advisors.py
│   ├── themes.py
│   ├── home.py
│   ├── upload.py
│   ├── predictions.py
│   └── about.py
├── config/
│   ├── client_template.json
│   ├── app_config.json
│   └── api_config.json    # protégé / .gitignore (ne pas publier)
├── assets/
│   ├── default_logo.png
│   └── icons/
├── requirements.txt
├── README.md              # ce fichier
└── resume_documents_financiers.ipynb

---

Installation (développeurs / déploiement interne)

«Pour les équipes techniques (pas pour le client final) — l’app est pensée pour être déployée par Alinyxe :»

1. Cloner le repo MASTER :

git clone <votre-repo>
cd alinyxe_master

2. Créer et activer un environnement Python :

python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

3. Installer les dépendances :

pip install -r requirements.txt

4. (Déploiement) Configurer les variables d’environnement / secrets côté serveur

   - Ne pas ajouter de clé API dans le repo.
   - Placer "api_config.json" ou variables d’environnement dans l’environnement serveur (ex. secrets manager, .streamlit/secrets.toml, ou variables d’environnement du service d’hébergement).

5. Lancer l’application (local / test) :

streamlit run app/main.py

---

Utilisation (client final)

Le client n’a rien à configurer. À l’ouverture de l’application il peut :

1. "Upload" — déposer un PDF, CSV ou Excel.
2. "Prédictions" — sélectionner une colonne cible et lancer une régression simple.
3. "Dashboard" — visualiser KPIs, tendances et télécharger les données.
4. "Chat" — poser des questions contextuelles ; l’IA répond en se basant sur les documents chargés et l’historique.
5. "Conseils IA" — lire les recommandations automatiques générées depuis les KPI.

---

Bonnes pratiques & limites

- Données sensibles : ne transférez pas de documents protégés sans accord.
- Taille des documents : limiter la taille pour éviter les dépassements de quota.
- Vérification humaine : toute recommandation IA doit être validée par un analyste avant décision critique.

---

Développement & extension

- MASTER → CLIENT : utiliser "scripts/create_client_app.py" pour générer une version client verrouillée et brandée (logo, couleurs, texte).
- Ajouts futurs : exports PDF/PowerPoint, analyses prescriptives avancées, intégrations ERP/CRM, retrieval+LLM pour réponses mieux sourcées.

---

Contacts & support

- Équipe technique Alinyxe — responsable projet : BATOLA KISSADI Manace Dalvy Gates
- Pour support/déploiement interne : "devops@alinyxe.ai" (ou contacter le responsable en interne)

---

Licence & confidentialité

Le code MASTER est la propriété d’Alinyxe. Ne pas publier le fichier "config/api_config.json" ni les clés sur un dépôt public. Mettre "api_config.json" dans ".gitignore".

---

Prêt à l’emploi — l’application est conçue pour être livrée clé en main : le client se connecte, utilise l’outil, et n’a aucune visibilité ni contrôle sur les paramètres techniques ou les clés API.

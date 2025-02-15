# 🎵 Spotify Data Scraping & Analysis  

## 📌 Description du Projet  

Ce projet vise à **scraper des données Spotify** et à réaliser une **analyse exploratoire (EDA)** pour identifier les tendances musicales. Il comprend :  

- **Scraping de playlists Spotify** (Top 50 France, USA, Maroc, etc.)
  
- **Analyse des données musicales** (popularité, genres dominants, corrélations)
   
- **Interface Flask** pour afficher et explorer les données
  
- **Visualisation avec Dash et Plotly**  

---

## 📂 Structure du Projet  
📦 spotify_scraping_project 

├── data/ # Données brutes et traitées

├── notebooks/ # Scripts Jupyter Notebook pour l'analyse

├── flask_app/ # Application Flask pour visualiser les données 

├── reports/ # Rapports et visualisations 

├── scraping/ # Scripts de scraping (Spotipy API) 

├── requirements.txt # Dépendances du projet 

├── README.md # Documentation du projet



---

## ⚡ Prérequis  

Avant de commencer, assure-toi d’avoir : 

✅ **Python 3.x** installé  

✅ Une clé API Spotify (Client ID & Client Secret)  

✅ Les bibliothèques nécessaires installées :  


pip install -r requirements.txt

## 🚀 Installation et Exécution

1️⃣ Cloner le projet


git clone https://github.com/Marwa-Drief/spotify_scraping.git

cd spotify_scraping

2️⃣ Configurer l’API Spotify

Crée un fichier .env et ajoute :


SPOTIPY_CLIENT_ID="ton_client_id"

SPOTIPY_CLIENT_SECRET="ton_client_secret"

3️⃣ Lancer le scraping

python scraping/scrape_spotify.py

4️⃣ Exécuter l’analyse exploratoire

jupyter notebook notebooks/data_analysis.ipynb

5️⃣ Lancer l’application Flask

cd flask_app
python app.py

🔗 Accès : http://localhost:5000

📊 Fonctionnalités Principales

✅ Scraping des données musicales Spotify

✅ Analyse exploratoire des tendances musicales

✅ Interface web Flask pour explorer les données

✅ Visualisations interactives avec Dash & Plotly

✅ Export des données en CSV

🛠️ Défis et Contraintes

⚠ Limites de l’API Spotify : Restrictions sur le nombre de requêtes

⚠ Changements de structure HTML : Adaptation des scripts en cas de modifications de Spotify

⚠ Temps de scraping : Optimisation nécessaire pour les grandes quantités de données

👥 Équipe

👩‍💻 Marwa Drief

👩‍💻 Safaa Ait Benlaassel

👩‍💻 Sara Idzim

👩‍💻 Salma Kaddouri

📌 Projet réalisé dans le cadre du parcours ICSD

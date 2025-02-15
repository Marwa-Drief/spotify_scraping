import csv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Identifiants d'authentification Spotify
CLIENT_ID = "4dcf1a0155e5437bb1b478fa06806163"  # Remplacez par vos identifiants
CLIENT_SECRET = "eba618cce6d74cddb050bd2c8fead8ee"
REDIRECT_URI = "http://localhost:8888/callback"

# Authentification avec Spotify
scope = "playlist-read-private"
spotify = Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                            client_secret=CLIENT_SECRET,
                                            redirect_uri=REDIRECT_URI,
                                            scope=scope))

# Liste des IDs des playlists et leurs noms correspondants
playlists = {
    "11dQ20IwNB5EtxcNtqTkp2": "Top 50 France",
    "5mm27PjceudJGmf31HtFeQ": "Top 50 USA",
    "5zS7qEBSr8r70iM7UKaVkS": "Top 50 Maroc",
    "3heplR0p1iTWLXBhd3KuDi": "Ma playlist"
}

# Fonction pour récupérer les morceaux d'une playlist
def get_playlist_tracks(playlist_id, playlist_name):
    tracks = []
    results = spotify.playlist_tracks(playlist_id)
    items = results['items']
    
    for i, item in enumerate(items):
        track = item['track']
        tracks.append({
            "Nom de la playlist": playlist_name,
            "Popularité": i + 1,
            "Nom du morceau": track['name'],
            "Artiste": ', '.join(artist['name'] for artist in track['artists']),

        })
    return tracks

# Collecter les données de toutes les playlists
all_tracks = []
for playlist_id, playlist_name in playlists.items():
    try:
        all_tracks.extend(get_playlist_tracks(playlist_id, playlist_name))
        print(f"Données récupérées pour la playlist : {playlist_name}")
    except Exception as e:
        print(f"Erreur pour la playlist {playlist_name} : {e}")

# Sauvegarde dans un fichier CSV
csv_filename = "morceaux_par_playlists.csv"
with open(csv_filename, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=all_tracks[0].keys())
    writer.writeheader()
    writer.writerows(all_tracks)

print(f"Les données ont été sauvegardées dans {csv_filename}")

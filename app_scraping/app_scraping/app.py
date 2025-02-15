from flask import Flask, render_template, request, jsonify, send_file
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from io import StringIO, BytesIO
from datetime import datetime

app = Flask(__name__)

# Configuration Spotify
CLIENT_ID = "20f14723e9cf44b7866b885bac777a6d"
CLIENT_SECRET = "1a8b3a9ae85a408e86e71ac893024831"

# Authentification Spotify
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
spotify = Spotify(auth_manager=auth_manager)

# Cache pour les résultats
search_cache = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    
    # Vérifier le cache
    if keyword in search_cache:
        return search_cache[keyword]
    
    try:
        results = spotify.search(q=keyword, type='artist', limit=1)
        
        if results['artists']['items']:
            artist = results['artists']['items'][0]
            artist_details = spotify.artist(artist['id'])
            top_tracks = spotify.artist_top_tracks(artist['id'])['tracks']
            
            tracks = []
            popularities = []
            
            for track in top_tracks:
                track_info = {
                    'name': track['name'],
                    'url': track['external_urls']['spotify'],
                    'popularity': track['popularity'],
                    'preview_url': track['preview_url'],
                    'album': track['album']['name'],
                    'release_date': track['album']['release_date'],
                    'duration_ms': track['duration_ms'],
                    'explicit': track['explicit']
                }
                tracks.append(track_info)
                popularities.append(track['popularity'])
            
            # Statistiques
            avg_popularity = sum(popularities) / len(popularities)
            latest_track = max(tracks, key=lambda x: x['release_date'])
            genres = artist_details['genres']
            
            result = render_template('index.html',
                                  artist=artist['name'],
                                  tracks=tracks,
                                  avg_popularity=round(avg_popularity, 1),
                                  latest_release=latest_track['release_date'],
                                  genres=genres)
            
            # Mettre en cache les informations sous forme de dictionnaire structuré pour l'export
            search_cache[keyword] = {
                'artist': artist['name'],
                'avg_popularity': round(avg_popularity, 1),
                'latest_release': latest_track['release_date'],
                'genres': ', '.join(genres),
                'tracks': tracks
            }
            return result
            
        return render_template('index.html', error="Aucun artiste trouvé")
        
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/export-csv')
def export_csv():
    if not search_cache:
        return "Pas de données à exporter", 404
    
    # Convertir les dernières données mises en cache en DataFrame
    cached_data = search_cache.get(list(search_cache.keys())[-1])
    tracks_data = cached_data['tracks'] if cached_data else []

    # Créer un DataFrame à partir des informations des pistes
    df = pd.DataFrame(tracks_data)
    
    if df.empty:
        return "Aucune donnée de piste à exporter", 404
    
    # Convertir le DataFrame en CSV et l'envoyer sous forme de fichier
    si = StringIO()
    df.to_csv(si, index=False)
    
    # Déplacer le curseur au début du StringIO
    si.seek(0)
    
    # Convertir StringIO en BytesIO
    byte_data = BytesIO(si.getvalue().encode())
    
    return send_file(
        byte_data,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'spotify_data_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'
    )

@app.route('/analytics/<artist_id>')
def get_analytics(artist_id):
    try:
        # Récupérer les analyses détaillées
        artist = spotify.artist(artist_id)
        top_tracks = spotify.artist_top_tracks(artist_id)['tracks']
        related_artists = spotify.artist_related_artists(artist_id)['artists']
        
        analytics = {
            'artist': artist['name'],
            'popularity': artist['popularity'],
            'followers': artist['followers']['total'],
            'genres': artist['genres'],
            'top_tracks': [{
                'name': track['name'],
                'popularity': track['popularity']
            } for track in top_tracks],
            'related_artists': [{
                'name': artist['name'],
                'popularity': artist['popularity']
            } for artist in related_artists[:5]]
        }
        
        return jsonify(analytics)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

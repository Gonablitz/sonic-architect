import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Setup Connection
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

def simple_test(q):
    print(f"Testing API with search query: {q}")
    results = sp.search(q=q, limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        return {
            "Name": track['name'],
            "Artist": track['artists'][0]['name'],
            "ID": track['id']
        }
    return "No results."

print(simple_test("Blinding Lights"))
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

def check_access():
    print("Testing basic metadata access...")
    results = sp.search(q="Blinding Lights", limit=1)
    if results['tracks']['items']:
        name = results['tracks']['items'][0]['name']
        print(f"✅ SEARCH SUCCESS: Found '{name}'")
        print("Note: The 403 only applies to 'Features'. Metadata is still open!")
    else:
        print("❌ Search failed.")

check_access()
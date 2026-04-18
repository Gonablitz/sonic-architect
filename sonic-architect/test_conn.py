import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def test_spotify():
    try:
        # This automatically looks for SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET
        auth_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        # Try to search for a track to verify the connection
        results = sp.search(q='track:Seven Nation Army', limit=1)
        track_name = results['tracks']['items'][0]['name']
        
        print(f"✅ CONNECTION SUCCESSFUL!")
        print(f"Found track: {track_name}")
        
    except Exception as e:
        print(f"❌ CONNECTION FAILED")
        print(f"Error: {e}")

if __name__ == "__main__":
    test_spotify()
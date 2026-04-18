import os
import librosa
import numpy as np
import psycopg2
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# 1. SETUP & AUTH
load_dotenv()
conn = psycopg2.connect(
    dbname="sonic_analytics",
    user="gmt_admin",
    password="neon_password",
    host="db_warehouse" # Use service name from docker-compose
)
cur = conn.cursor()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

def process_track(track_name, artist_name):
    # --- INGESTION (BRONZE) ---
    query = f"track:{track_name} artist:{artist_name}"
    results = sp.search(q=query, type='track', limit=1)
    
    if not results['tracks']['items']:
        print("❌ Signal Lost: Track not found.")
        return

    track = results['tracks']['items'][0]
    s_id = track['id']
    preview_url = track['preview_url']

    # Save to Bronze
    cur.execute("INSERT INTO tracks_raw (spotify_id, raw_json) VALUES (%s, %s) ON CONFLICT DO NOTHING", 
                (s_id, psycopg2.extras.Json(track)))
    
    if not preview_url:
        print(f"⚠️ No audio preview for {track_name}. Skipping DSP.")
        return

    # --- DSP ANALYSIS (SILER) ---
    print(f"🛰️ Processing Audio: {track_name}...")
    # (Simplified analysis for brevity - using the logic from our dsp_test.py)
    y, sr = librosa.load(preview_url)
    energy = np.mean(librosa.feature.rms(y=y))
    centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    
    # Calculate Sub-Bass (20-60Hz)
    stft = np.abs(librosa.stft(y))
    freqs = librosa.fft_frequencies(sr=sr)
    bass_mask = (freqs >= 20) & (freqs <= 60)
    bass_energy = np.mean(stft[bass_mask, :])

    # --- SAVE TO WAREHOUSE (GOLD) ---
    cur.execute("""
        INSERT INTO tracks_processed 
        (spotify_id, title, artist, energy_score, mellow_factor, sub_bass_peak)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (s_id, track['name'], track['artists'][0]['name'], float(energy), float(centroid), float(bass_energy)))
    
    conn.commit()
    print(f"✅ {track_name} archived in GMT_OS Database.")

if __name__ == "__main__":
    # Test it with a heavy-hitter
    process_track("Redbone", "Childish Gambino")
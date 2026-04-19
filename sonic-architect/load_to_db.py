import librosa
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from rich.console import Console

console = Console()

# 1. Database Connection (Standard SQLite File)
DB_URL = "sqlite:///sonic_vault.db"
engine = create_engine(DB_URL)

def run_etl_pipeline(file_path):
   def run_etl_pipeline(file_path):
    y, sr = librosa.load(file_path)

    # --- Advanced Audio Engineering Metrics ---
    
    # 1. Perceived Loudness (LUFS approximation)
    rms = librosa.feature.rms(y=y)
    loudness_db = librosa.amplitude_to_db([np.mean(rms)], ref=np.max)[0]

    # 2. Spectral Flatness (0.0 = Tonal/Musical, 1.0 = White Noise/Distortion)
    flatness = np.mean(librosa.feature.spectral_flatness(y=y))

    # 3. Harmonic vs Percussive Ratio (Producer's Balance)
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    h_p_ratio = np.mean(y_harmonic) / np.mean(y_percussive)

    # 4. Tempo & Rhythm Stability
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    processed_data = {
        "track_title": file_path.replace(".mp3", "").replace("_", " "),
        "bpm": round(float(tempo), 1),
        "loudness_lufs": round(float(loudness_db), 2),
        "timbre_texture": "Smooth" if flatness < 0.1 else "Aggressive/Noisy",
        "tonal_purity": round(float(1 - flatness), 3),
        "harmonic_bias": round(float(h_p_ratio), 2),
        "processed_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    
    df = pd.DataFrame([processed_data])
    
    try:
        df.to_sql('tracks_processed', engine, if_exists='append', index=False)
        print(f"✅ Data secured for: {file_path}")
    except Exception as e:
        print(f"❌ Load failed: {e}")

# test
if __name__ == "__main__":
    
    run_etl_pipeline("The_Weeknd_Blinding_Lights.mp3", "https://youtube.com/watch?v=example")
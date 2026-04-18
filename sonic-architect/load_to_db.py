import librosa
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from rich.console import Console

console = Console()

# 1. Database Connection (Standard SQLite File)
# This creates a file named 'sonic_vault.db' in your current folder
DB_URL = "sqlite:///sonic_vault.db"
engine = create_engine(DB_URL)

def run_etl_pipeline(file_path, video_url=None):
    console.print(f"[bold cyan]🚀 Initializing Sonic Vault ETL:[/bold cyan] {file_path}")
    
    y, sr = librosa.load(file_path, sr=None)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    rms = librosa.feature.rms(y=y)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    
# In load_to_db.py
processed_data = {
    "track_title": file_path.split('.')[0],
    "artist_name": "Local Analysis",
    "bpm": round(float(np.mean(tempo)), 2),
    "energy_score": round(float(np.mean(rms)), 4),
    "sub_bass_peak": round(float(np.mean(centroid)), 2),
    "youtube_url": video_url,  # THIS MUST BE A REAL STRING
    "processed_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
}
    
    df = pd.DataFrame([processed_data])
    
    try:
        df.to_sql('tracks_processed', engine, if_exists='append', index=False)
        console.print("[bold green]✅ DATA SECURED WITH SOURCE URL[/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ LOAD FAILED:[/bold red] {e}")
run_etl_pipeline("track.mp3")
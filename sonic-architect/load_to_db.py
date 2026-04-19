import librosa
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from rich.console import Console

console = Console()

# 1. Database Connection (Standard SQLite File)
DB_URL = "sqlite:///sonic_vault.db"
engine = create_engine(DB_URL)

def run_etl_pipeline(file_path, video_url=None):
    console.print(f"[bold cyan]🚀 Initializing Sonic Vault ETL:[/bold cyan] {file_path}")
    
    # Load and analyze audio
    y, sr = librosa.load(file_path, sr=None)
    
    #  (tempo, beats)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    rms = librosa.feature.rms(y=y)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    
    
    processed_data = {
        "track_title": file_path.split('.')[0].replace("_", " "),
        "artist_name": "Local Analysis",
        "bpm": round(float(tempo), 2),  
        "energy_score": round(float(np.mean(rms)), 4),
        "sub_bass_peak": round(float(np.mean(centroid)), 2),
        "youtube_url": video_url,  
        "processed_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    df = pd.DataFrame([processed_data])
    
    try:
        df.to_sql('tracks_processed', engine, if_exists='append', index=False)
        console.print(f"[bold green]✅ DATA SECURED FOR:[/bold green] {processed_data['track_title']}")
    except Exception as e:
        console.print(f"[bold red]❌ LOAD FAILED:[/bold red] {e}")

# test
if __name__ == "__main__":
    
    run_etl_pipeline("The_Weeknd_Blinding_Lights.mp3", "https://youtube.com/watch?v=example")
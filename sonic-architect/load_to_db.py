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
    # ... logic for tempo and centroid ...
    
    processed_data = {
        "track_title": file_path.split('.')[0].replace("_", " "),
        "artist_name": "Local Analysis",
        "bpm": round(float(tempo), 2),  
        "energy_score": round(float(np.mean(rms)), 4),
        "sub_bass_peak": round(float(np.mean(centroid)), 2),
        "youtube_url": "N/A",  
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
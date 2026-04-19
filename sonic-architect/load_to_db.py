import librosa
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from rich.console import Console

console = Console()
DB_URL = "sqlite:///sonic_vault.db"
engine = create_engine(DB_URL)

def run_etl_pipeline(file_path, video_url="N/A"):
    console.print(f"[bold yellow]⚙️ Extracting Engineering Metrics...[/bold yellow]")
    
    # Load audio
    y, sr = librosa.load(file_path)

    # --- 1. Average Loudness (RMS) ---
    # Important for the 'Loudness War' perspective
    rms = librosa.feature.rms(y=y)
    loudness_db = librosa.amplitude_to_db([np.mean(rms)], ref=np.max)[0]

    # --- 2. Spectral Flatness ---
    # 0.0 = pure tone (flute/synth), 1.0 = noise (snare/distortion)
    flatness = np.mean(librosa.feature.spectral_flatness(y=y))

    # --- 3. Harmonic vs Percussive Separation (HPSS) ---
    # Separates the 'musical' parts from the 'drums'
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    h_p_ratio = np.mean(np.abs(y_harmonic)) / np.mean(np.abs(y_percussive))

    # --- 4. Tempo Tracking ---
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    processed_data = {
        "track_title": file_path.replace(".mp3", "").replace("_", " "),
        "artist_name": "Studio Analysis",
        "bpm": round(float(tempo), 1),
        "energy_score": round(float(loudness_db), 2), # Mapping loudness to your UI energy column
        "sub_bass_peak": round(float(1 - flatness), 3), # Mapping purity to your UI bass column
        "youtube_url": video_url,
        "processed_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    df = pd.DataFrame([processed_data])
    
    try:
        df.to_sql('tracks_processed', engine, if_exists='append', index=False)
        console.print(f"[bold green]✅ SONIC DATA SECURED:[/bold green] {processed_data['track_title']}")
    except Exception as e:
        console.print(f"[bold red]❌ LOAD FAILED:[/bold red] {e}")

if __name__ == "__main__":
    # Test call
    run_etl_pipeline("The_Weeknd_Blinding_Lights.mp3", "https://youtube.com/watch?v=4NRXx6U8ABQ")
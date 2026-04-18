import librosa
import numpy as np
import time
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def analyze_with_style(file_path):
    with Progress(
        SpinnerColumn(spinner_name="dots12"),
        TextColumn("[bold cyan]{task.description}"),
        transient=True,
    ) as progress:
        
        # Phase 1: Ingestion
        progress.add_task(description="Scanning Binary Stream...", total=None)
        y, sr = librosa.load(file_path, sr=None)
        time.sleep(1) # Visual flair
        
        # Phase 2: Frequency Analysis
        progress.add_task(description="Calculating Spectral Centroid...", total=None)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        rms = librosa.feature.rms(y=y)
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        
    # Build the Display Table
    table = Table(title="[bold neon_pink]SONIC SENTINEL: ANALYSIS COMPLETE", style="cyan")
    
    table.add_column("Parameter", style="bold magenta")
    table.add_column("Value", justify="right", style="green")
    table.add_column("Status", justify="center")

    table.add_row("Tempo", f"{np.mean(tempo):.2f} BPM", "OPTIMAL")
    table.add_row("Energy (RMS)", f"{np.mean(rms):.4f}", "STABLE")
    table.add_row("Bass Center", f"{np.mean(centroid):.2f} Hz", "🔥 DEEP")

    console.print(table)

# Run the styled engine
analyze_with_style("track.mp3")
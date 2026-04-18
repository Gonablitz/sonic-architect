import sqlite3
import pandas as pd
from rich.console import Console
from rich.table import Table

console = Console()

def display_leaderboard():
    # 1. Connect to your local vault
    conn = sqlite3.connect('sonic_vault.db')
    
    # 2. Query the data, ranking by sub_bass_peak (lowest centroid = deepest bass)
    query = "SELECT track_title, bpm, energy_score, sub_bass_peak FROM tracks_processed ORDER BY sub_bass_peak ASC"
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        console.print("[bold red]Vault is empty! Harvest some tracks first.[/bold red]")
        return

    # 3. Build a Cyber-styled table
    table = Table(title="[bold cyan]SONIC ARCHITECT: BASS LEADERBOARD", style="magenta")
    
    table.add_column("Rank", justify="center", style="dim")
    table.add_column("Track Title", style="bold white")
    table.add_column("BPM", justify="right", style="green")
    table.add_column("Energy", justify="right", style="yellow")
    table.add_column("Bass Profile (Hz)", justify="right", style="cyan")
    table.add_column("Optimization Tag", justify="center")

    for i, row in df.iterrows():
        # Optimization logic: Lower Hz means deeper bass
        tag = "🔥 DEEP BASS" if row['sub_bass_peak'] < 1500 else "⚡ BRIGHT"
        if row['bpm'] > 140: tag = "🚀 OVERCLOCKED"
        
        table.add_row(
            str(i + 1),
            row['track_title'],
            f"{row['bpm']:.1f}",
            f"{row['energy_score']:.3f}",
            f"{row['sub_bass_peak']:.1f}",
            tag
        )

    console.print(table)

if __name__ == "__main__":
    display_leaderboard()
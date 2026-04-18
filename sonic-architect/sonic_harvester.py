import yt_dlp
import os
from rich.console import Console

console = Console()

def harvest_audio(query):
    console.print(f"[bold cyan]🛰️ Initializing YouTube Fallback for:[/bold cyan] {query}")
    
    # Options for high-quality audio-only download
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{query.replace(" ", "_")}.%(ext)s',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{query} audio"])
        console.print(f"[bold green]✅ Harvested:[/bold green] {query}.mp3")
    except Exception as e:
        console.print(f"[bold red]❌ Harvest Failed:[/bold red] {e}")

# Try harvesting a track the Spotify API blocked
harvest_audio("The Weeknd Blinding Lights")
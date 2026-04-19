import yt_dlp
import os
from rich.console import Console

console = Console()

def harvest_audio(query):
    console.print(f"[bold cyan]🛰️ Initializing YouTube Fallback for:[/bold cyan] {query}")
    
    file_name = query.replace(" ", "_")
    
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'./{file_name}.%(ext)s', 
        'quiet': True,
        'nocheckcertificate': True,
        # PIVOT: Using web clients instead of iOS to avoid PO Token requirement
        'extractor_args': {
            'youtube': {
                'player_client': ['web', 'mweb'],
                'skip': ['dash', 'hls'] # Skip complex streaming formats
            }
        },
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{query} audio"])
        
        expected_file = f"{file_name}.mp3"
        console.print(f"[bold green]✅ Harvested:[/bold green] {expected_file}")
        
        
        return expected_file
        
    except Exception as e:
        console.print(f"[bold red]❌ Harvest Failed:[/bold red] {e}")
        return None
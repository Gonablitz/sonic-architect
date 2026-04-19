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
        # THE BYPASS
        'nocheckcertificate': True,
        'extractor_args': {'youtube': {'player_client': ['ios']}},
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
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
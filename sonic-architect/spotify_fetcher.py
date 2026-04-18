import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from rich.console import Console
from dotenv import load_dotenv 

# Load variables from .env file
load_dotenv()
console = Console()

# Setup Connection
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

def fetch_and_analyze(query):
    console.print(f"[bold cyan]🔍 Searching Spotify for:[/bold cyan] {query}")
    
    results = sp.search(q=query, limit=1, type='track')
    if not results['tracks']['items']:
        console.print("[bold red]❌ Track not found on Spotify.[/bold red]")
        return

    track = results['tracks']['items'][0]
    
    # SAFE CHECK: Use .get() to avoid KeyError
    preview_url = track.get('preview_url')
    track_name = track['name'].replace(" ", "_")

    if not preview_url:
        console.print(f"[bold yellow]⚠️ No preview available for '{track['name']}'.[/bold yellow]")
        console.print("[italic]Spotify restricts previews for some regions or tracks.[/italic]")
        console.print("💡 [bold]Try searching for 'Blinding Lights' or 'The Weeknd' tracks; they usually have previews.[/bold]")
        return

    # 2. Download the audio clip
    console.print(f"[bold green]📥 Found Preview![/bold green] Downloading {track['name']}...")
    response = requests.get(preview_url)
    filename = f"{track_name}.mp3"

    with open(filename, 'wb') as f:
        f.write(response.content)

    console.print(f"✅ Saved to [bold white]{filename}[/bold white].")
    console.print(f"[bold cyan]🔍 Searching Spotify for:[/bold cyan] {query}")
    
    # 1. Search for the track
    results = sp.search(q=query, limit=1, type='track')
    if not results['tracks']['items']:
        console.print("[bold red]❌ Track not found on Spotify.[/bold red]")
        return

    track = results['tracks']['items'][0]
    track_name = track['name'].replace(" ", "_")
    preview_url = track['preview_url']

    if not preview_url:
        console.print(f"[bold yellow]⚠️ No preview available for '{track['name']}'.[/bold yellow]")
        console.print("Try a more popular track (e.g., 'Blinding Lights').")
        return

    # 2. Download the audio clip
    console.print(f"[bold green]📥 Found Preview![/bold green] Downloading {track['name']}...")
    response = requests.get(preview_url)
    filename = f"{track_name}.mp3"

    with open(filename, 'wb') as f:
        f.write(response.content)

    console.print(f"✅ Saved to [bold white]{filename}[/bold white]. The Sentinel will now take over!")

# Test it
fetch_and_analyze("The Weeknd Blinding Lights")
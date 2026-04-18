import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rich.console import Console
from load_to_db import run_etl_pipeline 
from visualize_sonic import generate_visuals

console = Console()

class AudioDropHandler(FileSystemEventHandler):
    
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.mp3'):
            file_name = os.path.basename(event.src_path)
            
            
            target_url = None 
            
            try:
                
                run_etl_pipeline(file_name, video_url=target_url)
                
                # 2. Visualize
                img_name = f"{file_name.rsplit('.', 1)[0]}.png"
                generate_visuals(file_name, img_name)
                
                console.print(f"[bold green]✨ {file_name} synced to vault.[/bold green]")
            except Exception as e:
                console.print(f"[bold red]❌ Sentinel Error:[/bold red] {e}")
if __name__ == "__main__":
    path = "." 
    event_handler = AudioDropHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    
    console.print("[bold cyan]🛡️ SONIC SENTINEL ACTIVE...[/bold cyan]")
    console.print("[italic]Monitoring folder for new frequency streams...[/italic]\n")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
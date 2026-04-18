# Create a quick file: check_all.py
import spotipy
import librosa
import pandas as pd
import numpy as np

print("--- SONIC SENTINEL SYSTEM CHECK ---")
print(f"✅ Spotify API Library: {spotipy.__version__}")
print(f"✅ Audio Analysis (Librosa): {librosa.__version__}")
print(f"✅ Data Engine (Pandas): {pd.__version__}")
print("--- ALL SYSTEMS ONLINE ---")
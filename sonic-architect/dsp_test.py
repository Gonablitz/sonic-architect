import librosa
import numpy as np
import requests

def analyze_vibe(audio_url):
    print("🛰️ Downloading signal...")
    r = requests.get(audio_url)
    with open("temp.mp3", "wb") as f:
        f.write(r.content)

    print("🧠 Analyzing Audio DNA...")
    # Load the audio file
    y, sr = librosa.load("temp.mp3")

    # 1. Calculate the "Bass Punch" (Root Mean Square Energy)
    rms = librosa.feature.rms(y=y)
    avg_energy = np.mean(rms)

    # 2. Calculate "Brightness" (Spectral Centroid)
    # Higher = more 'shimmer', Lower = more 'deep/mellow'
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    avg_centroid = np.mean(centroid)

    print(f"--- GMT_OS ANALYTICS ---")
    print(f"Energy Score: {avg_energy:.4f}")
    print(f"Mellow/Bright Factor: {avg_centroid:.2f} Hz")
    
    if avg_centroid < 1500:
        print("Verdict: Deep Neo-Soul Vibe detected.")
    else:
        print("Verdict: High-Energy/Pop Vibe detected.")

if __name__ == "__main__":
    # A sample preview URL (You can replace this with a real Spotify preview link later)
    test_url = "https://p.scdn.co/mp3-preview/3103239a9c927f1cfd1d867c293796ec12a1491d?cid=774b75d31190470c91030f2874135e6c"
    analyze_vibe(test_url)
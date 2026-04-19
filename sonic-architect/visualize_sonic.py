import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_visuals(file_path):
    # Use 'offset' and 'duration' if you want to analyze just the "drop" (e.g., first 30s)
    y, sr = librosa.load(file_path, duration=60) 
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))

    # --- 1. Harmonic Fingerprint (Chromagram) ---
    # Enhanced with CQT (Constant-Q Transform) for better musical pitch resolution
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', ax=ax1, cmap='magma')
    ax1.set_title('🎼 Harmonic Content (Note Distribution)', fontsize=16, color='#00FFCC')
    ax1.set_ylabel('Pitch Class')

    # --- 2. Power Spectral Density (The Mix Balance) ---
    # Using a Mel-scaled Power Spectrogram (matches human hearing)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, ax=ax2, cmap='viridis')
    ax2.set_title('🔊 Power Spectral Density (Frequency Weighting)', fontsize=16, color='#00FFCC')
    ax2.set_ylabel('Frequency (Hz)')
    
    plt.colorbar(img, ax=ax2, format="%+2.0f dB")
    plt.tight_layout()
    
    # Save as PNG for the Streamlit UI
    output_path = file_path.replace(".mp3", ".png")
    plt.savefig(output_path, dpi=150)
    plt.close()

if __name__ == "__main__":
    
    test_file = "The_Weeknd_Blinding_Lights.mp3"
    if os.path.exists(test_file):
        generate_visuals(test_file)
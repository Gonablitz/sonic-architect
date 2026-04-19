import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_visuals(file_path):
   
    # 1. Safety Check: Does the file actually exist?
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found.")
        return

    # 2. Load the specific track provided by the Sentinel
    y, sr = librosa.load(file_path)

    # 3. Create the Figure with the Cyberpunk theme
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(12, 8))

    # --- Top Subplot: Waveform ---
    plt.subplot(2, 1, 1)
    librosa.display.waveshow(y, sr=sr, color='cyan', alpha=0.8)
    plt.title(f'Sonic Sentinel: Waveform Analysis ({file_path})', color='white')
    plt.ylabel('Amplitude')

    # --- Bottom Subplot: Spectrogram ---
    plt.subplot(2, 1, 2)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    img = librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz', cmap='magma')
    plt.title('Sonic Sentinel: Frequency Spectrogram', color='white')
    plt.colorbar(img, format='%+2.0f dB')

    plt.tight_layout()
    
    
    output_name = file_path.replace(".mp3", ".png")
    plt.savefig(output_name)
    plt.close(fig)
    
    print(f"✅ Visualization secured as '{output_name}'")


if __name__ == "__main__":
    
    test_file = "The_Weeknd_Blinding_Lights.mp3"
    if os.path.exists(test_file):
        generate_visuals(test_file)
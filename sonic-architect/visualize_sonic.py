import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# 1. Load the track
y, sr = librosa.load("track.mp3")

# 2. Create the Figure
plt.figure(figsize=(12, 8))

# --- Top Subplot: Waveform ---
plt.subplot(2, 1, 1)
librosa.display.waveshow(y, sr=sr, color='cyan', alpha=0.8)
plt.title('Sonic Sentinel: Waveform Analysis', color='white')
plt.ylabel('Amplitude')

# --- Bottom Subplot: Spectrogram ---
plt.subplot(2, 1, 2)
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='hz', cmap='magma')
plt.title('Sonic Sentinel: Frequency Spectrogram', color='white')
plt.colorbar(format='%+2.0f dB')

lt.tight_layout()
plt.style.use('dark_background')
plt.savefig('sonic_analysis.png')
print("✅ Visualization saved as 'sonic_analysis.png'!")
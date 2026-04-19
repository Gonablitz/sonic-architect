import streamlit as st
import sqlite3
import pandas as pd
import os
import time
from sonic_harvester import harvest_audio
from load_to_db import run_etl_pipeline
from visualize_sonic import generate_visuals

# --- THEME & UI CONFIG ---
st.set_page_config(page_title="Sonic Architect | Engineering Vault", layout="wide")

# Custom CSS for a high-end Studio look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1a1c24; padding: 15px; border-radius: 10px; border: 1px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA FETCHING ---
def get_data():
    conn = sqlite3.connect('sonic_vault.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracks_processed (
            track_title TEXT, artist_name TEXT, bpm REAL, 
            energy_score REAL, sub_bass_peak REAL, 
            youtube_url TEXT, processed_at TEXT
        )
    """)
    conn.commit()
    try:
        df = pd.read_sql_query("SELECT * FROM tracks_processed ORDER BY processed_at DESC", conn)
    except Exception:
        df = pd.DataFrame(columns=["track_title", "artist_name", "bpm", "energy_score", "sub_bass_peak", "youtube_url", "processed_at"])
    conn.close()
    return df

# --- SIDEBAR: HARVESTER ---
st.sidebar.title("🎚️ Engineering Console")
search_query = st.sidebar.text_input("Source Track (Artist - Name)")

if st.sidebar.button("Begin Sonic Extraction"):
    if search_query:
        with st.spinner("🛰️ Extracting audio streams and spectral data..."):
            audio_file = harvest_audio(search_query) 
            if audio_file and os.path.exists(audio_file):
                run_etl_pipeline(audio_file)
                generate_visuals(audio_file)
                st.sidebar.success(f"✅ {search_query} Analyzed!")
                st.rerun()
            else:
                st.sidebar.error("❌ Extraction failed. Check FFmpeg logs.")

# --- MAIN UI ---
st.title("🎧 Sonic Architect: Multimedia Vault")
df = get_data()

if df.empty:
    st.info("Vault offline. Please harvest a track to initialize spectral analysis.")
else:
    # 1. Selection & Header
    selected_track = st.selectbox("Select Master Track:", df['track_title'].unique())
    track_info = df[df['track_title'] == selected_track].iloc[0]
    
    file_base = selected_track.replace(" ", "_")
    audio_path = f"{file_base}.mp3"
    img_path = f"{file_base}.png"

    # 2. PRODUCER METRICS (Top Row)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Tempo (BPM)", f"{track_info['bpm']:.1f}")
    with m2:
        st.metric("Sub-Bass Peak", f"{track_info['sub_bass_peak']:.1f} Hz")
    with m3:
        # Energy score repurposed as RMS Headroom/Loudness for the UI
        st.metric("RMS Energy", f"{track_info['energy_score']:.2f} dBFS")
    with m4:
        st.metric("Analyzed At", track_info['processed_at'].split()[0])

    # 3. ANALYSIS TABS
    tab1, tab2 = st.tabs(["📡 Spectral Analysis & Monitoring", "📺 Source Feed"])

    with tab1:
        col_img, col_audio = st.columns([2, 1])
        with col_img:
            if os.path.exists(img_path):
                st.image(img_path, caption="Top: Chromagram (Pitch Class) | Bottom: Mel-Spectrogram (Energy Density)")
            else:
                st.warning("Spectral scan missing for this track.")
        
        with col_audio:
            st.markdown("### 🎛️ Monitor Output")
            if os.path.exists(audio_path):
                st.audio(audio_path)
                st.download_button("Download Master", data=open(audio_path, 'rb'), file_name=audio_path)
            else:
                st.error("Audio buffer empty.")
            
            st.markdown("---")
            st.write("**Producer Notes:**")
            st.caption("Inspect the bottom spectrogram for 'muddy' frequencies in the 200-500Hz range. The top Chromagram indicates key stability for potential sampling.")

    with tab2:
        if track_info['youtube_url'] and "http" in str(track_info['youtube_url']):
            st.video(track_info['youtube_url'])
        else:
            st.link_button("View Source on YouTube", f"https://www.youtube.com/results?search_query={selected_track}")
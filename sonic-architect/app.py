import streamlit as st
import sqlite3
import pandas as pd
import os
import time
from sonic_harvester import harvest_audio
from load_to_db import run_etl_pipeline
from visualize_sonic import generate_visuals

st.set_page_config(page_title="Sonic Architect Vault", layout="wide")

# --- GLOBAL SEARCH SECTION ---
st.sidebar.header("📡 Global Search")
search_query = st.sidebar.text_input("Enter Song Name & Artist")

if st.sidebar.button("Harvest & Analyze"):
    if search_query:
        with st.spinner(f"🛰️ Harvesting..."):
            audio_file = harvest_audio(search_query) 
            
            
            if audio_file:
                st.sidebar.write(f"🔍 System found: {audio_file}")
            else:
                st.sidebar.error("❌ Harvester returned nothing. Check ffmpeg.")

            if audio_file and os.path.exists(audio_file):
                run_etl_pipeline(audio_file)
                generate_visuals(audio_file)
                st.rerun()
    else:
        st.sidebar.warning("Please enter a search term.")

# --- SIDEBAR: UTILITIES ---
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Vault Utilities")

if st.sidebar.button("🗑️ Clear Vault History", type="secondary"):
    try:
        conn = sqlite3.connect('sonic_vault.db')
        cursor = conn.cursor()
        
        # 1. Clear the SQL table
        cursor.execute("DELETE FROM tracks_processed")
        conn.commit()
        conn.close()
        
        # 2. Cleanup local assets 
        
        for file in os.listdir("."):
            if file.endswith(".png") or file.endswith(".mp3") or file.endswith(".mp4"):
                os.remove(file)
                
        st.sidebar.success("Vault purged successfully!")
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        st.sidebar.error(f"Purge failed: {e}")
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

df = get_data()

# --- . UI DYNAMIC INSPECTION AREA ---
# --- i. INVENTORY TABLE ---
st.markdown("### 📊 Audio Inventory")
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("Vault is currently empty. Use the sidebar to harvest new audio data.")

# --- ii. DYNAMIC INSPECTION & VIDEO STREAMING ---

if not df.empty:
    st.markdown("---")
    st.markdown("### 🔍 Multimedia Inspection")

    # 1. Selection
    options = df['track_title'].unique()
    selected_track = st.selectbox(
        "Select a track to inspect:", 
        options,
        key="inspection_selector"
    )

    # 2. Extract specific track info safely
    selection_filter = df[df['track_title'] == selected_track]
    
    if not selection_filter.empty:
        track_info = selection_filter.iloc[0]

        # File naming logic
        file_base = selected_track.replace(" ", "_")
        audio_path = f"{file_base}.mp3"
        img_path = f"{file_base}.png"

        # 3. Display Tabs
        tab1, tab2, tab3 = st.tabs(["📊 Stats & Audio", "📺 Source Video", "📡 Sonar Scan"])

        with tab1:
            col_l, col_r = st.columns(2)
            with col_l:
                if os.path.exists(audio_path):
                    st.audio(audio_path)
                else:
                    st.error("Audio file missing.")
            with col_r:
                st.write(f"**BPM:** {track_info['bpm']:.1f}")
                st.write(f"**Bass Peak:** {track_info['sub_bass_peak']:.1f} Hz")

        with tab2:
            yt_url = track_info.get('youtube_url')
            
            if yt_url and ("youtube.com" in str(yt_url) or "youtu.be" in str(yt_url)):
                st.video(yt_url)
            else:
                st.warning("⚠️ Direct embed link not found.")
                st.link_button("📺 Watch on YouTube", f"https://www.youtube.com/results?search_query={selected_track}")

        with tab3:
            if os.path.exists(img_path):
                st.image(img_path, use_column_width=True)
            else:
                st.info("Sonar Scan visualization not generated for this track.")
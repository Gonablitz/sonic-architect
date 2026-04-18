import streamlit as st
import sqlite3
import pandas as pd
import os
import time
from sonic_harvester import harvest_audio

st.set_page_config(page_title="Sonic Architect Vault", layout="wide")

# --- GLOBAL SEARCH SECTION ---
st.sidebar.header("📡 Global Search")
search_query = st.sidebar.text_input("Enter Song Name & Artist")

if st.sidebar.button("Harvest & Analyze"):
    if search_query:
        with st.spinner(f"🛰️ Harvesting '{search_query}' from the web..."):
            harvest_audio(search_query) # This drops the file
            time.sleep(6) # Give the Sentinel background service time to work
            st.sidebar.success(f"✅ {search_query} added to vault!")
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
        
        # 2. Cleanup local assets (Optional but recommended)
        # This removes all .png and .mp3 files so your folder stays tidy
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
    df = pd.read_sql_query("SELECT * FROM tracks_processed ORDER BY processed_at DESC", conn)
    conn.close()
    return df

df = get_data()

# --- 3. UI DYNAMIC INSPECTION AREA ---
# Only show this section if the vault actually has tracks!
if not df.empty:
    st.markdown("---")
    st.markdown("### 🔍 Multimedia Inspection")
    
    selected_track = st.selectbox("Select a track to inspect:", df['track_title'].unique())
    
    # This line was causing the error because it ran even when the DB was empty
    track_info = df[df['track_title'] == selected_track].iloc[0]

    # ... rest of your player/tabs code goes here ...
else:
    st.info("Vault is currently empty. Use the sidebar to harvest new audio data.")
    
    # 2. Inventory Table
    st.markdown("### 📊 Audio Inventory")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

# --- 3. DYNAMIC INSPECTION & VIDEO STREAMING ---
st.markdown("---")
st.markdown("### 🔍 Multimedia Inspection")

selected_track = st.selectbox(
    "Select a track to inspect:", 
    df['track_title'].unique(),
    key="inspection_selector"  # Add this unique ID
)

# Get the specific data for the selected track
track_info = df[df['track_title'] == selected_track].iloc[0]

# File naming logic
file_base = selected_track.replace(" ", "_")
audio_path = f"{file_base}.mp3"
img_path = f"{file_base}.png"

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
    url_from_db = track_info.get('youtube_url')
    
    if url_from_db and "youtube.com" in url_from_db:
        # Standard Streamlit video component for direct links
        st.video(url_from_db)
    else:
        st.error("🔒 YouTube restricted this embed.")
        # Create a direct link that opens in a new tab as a fallback
        track_query = selected_track.replace("_", " ")
        st.link_button("🚀 Open Video on YouTube", 
                       f"https://www.youtube.com/results?search_query={track_query}+official+audio")

with tab3:
    if os.path.exists(img_path):
        st.image(img_path, use_column_width=True)
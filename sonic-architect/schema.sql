-- Create the Core Tables
CREATE TABLE IF NOT EXISTS tracks_raw (
    id SERIAL PRIMARY KEY,
    spotify_id VARCHAR(100) UNIQUE,
    raw_json JSONB, -- The 'Bronze' layer: Store everything just in case
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tracks_processed (
    id SERIAL PRIMARY KEY,
    spotify_id VARCHAR(100) REFERENCES tracks_raw(spotify_id),
    title VARCHAR(255),
    artist VARCHAR(255),
    energy_score FLOAT,        -- From our DSP analysis
    mellow_factor FLOAT,       -- From our DSP analysis
    sub_bass_peak FLOAT,       -- 20Hz-60Hz intensity
    tempo FLOAT,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- The 'Gold' View: This is what powers your Dashboard
CREATE OR REPLACE VIEW v_sonic_insights AS
SELECT 
    artist,
    COUNT(*) as track_count,
    AVG(energy_score) as avg_energy,
    AVG(sub_bass_peak) as avg_bass_punch,
    CASE 
        WHEN AVG(mellow_factor) < 1500 THEN 'Deep Neo-Soul'
        ELSE 'High-End Pop/R&B'
    END as vibe_classification
FROM tracks_processed
GROUP BY artist;
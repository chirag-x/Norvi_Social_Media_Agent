ALTER TABLE scheduled_posts ADD COLUMN external_post_id TEXT;
ALTER TABLE scheduled_posts ADD COLUMN external_url TEXT;

-- For Phase 23 Content Series
CREATE TABLE IF NOT EXISTS content_series (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE extracted_clips ADD COLUMN series_id INTEGER REFERENCES content_series(id);
ALTER TABLE extracted_clips ADD COLUMN series_part INTEGER;

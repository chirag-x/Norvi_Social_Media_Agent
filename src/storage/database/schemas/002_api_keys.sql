CREATE TABLE api_keys (
    platform TEXT PRIMARY KEY,
    client_id TEXT,
    client_secret TEXT,
    access_token TEXT,
    refresh_token TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

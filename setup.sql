/*
Setup script to automatically create DB structure if it doesn't exist.
Script should be ran on bot startup, and will not affect any existing data
:*/

CREATE TABLE IF NOT EXISTS guilds (
    id INTEGER PRIMARY KEY UNIQUE,     -- discord id
    last_seen DATETIME
);

CREATE TABLE IF NOT EXISTS pins (
    id INTEGER PRIMARY KEY,
    type INTEGER NOT NULL,
    guild_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    FOREIGN KEY (guild_id) REFERENCES guilds(id) ON DELETE CASCADE ON UPDATE CASCADE
);

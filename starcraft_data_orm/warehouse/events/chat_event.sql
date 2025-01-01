CREATE TABLE IF NOT EXISTS events.chat_event (
    __id__ SERIAL PRIMARY KEY,          -- Auto-incrementing primary key

    pid INTEGER,                        -- Player ID
    frame INTEGER,                      -- Frame number at which the event occurred
    second INTEGER,                     -- Time in seconds
    name TEXT,                          -- Name of the chat event
    target INTEGER,                     -- Target of the chat (e.g., specific player ID)
    text TEXT,                          -- The chat message content
    to_all BOOLEAN,                     -- Whether the message was sent to all players
    to_allies BOOLEAN,                  -- Whether the message was sent to allies only
    to_observers BOOLEAN,               -- Whether the message was sent to observers only

    __player__ INTEGER,                 -- Foreign key to replay.PLAYER
    __info__ INTEGER,                   -- Foreign key to replay.INFO

    CONSTRAINT chat_event_player_fkey FOREIGN KEY (__player__)
        REFERENCES replay.PLAYER (__id__) ON DELETE SET NULL,
    CONSTRAINT chat_event_info_fkey FOREIGN KEY (__info__)
        REFERENCES replay.INFO (__id__) ON DELETE CASCADE
);

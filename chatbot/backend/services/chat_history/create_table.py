create_table_sql_query = """
CREATE TABLE conversations (
    conversation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL,
    conversation_title TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    feedback TEXT
);

CREATE TABLE messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    sender VARCHAR(10) CHECK (sender IN ('user', 'bot')),
    text TEXT NOT NULL,
    is_useful BOOLEAN, -- For Thumbs up Thumbs down
    created_at TIMESTAMP DEFAULT NOW()
);
"""
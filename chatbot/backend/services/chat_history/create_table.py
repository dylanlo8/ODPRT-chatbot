create_table_query = """
CREATE TABLE conversations (
    conversation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    is_guest BOOLEAN DEFAULT FALSE,
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
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE TABLE knowledge_base (
    document_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chunk_id UUID DEFAULT gen_random_uuid(),
    document_source TEXT NOT NULL,
    document_source_type VARCHAR(50) NOT NULL,
    image_url TEXT,
    source_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);

CREATE TABLE knowledge_base_analytics (
    analytics_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES knowledge_base(document_id) ON DELETE CASCADE,
    chunk_id UUID NOT NULL,
    conversation_id UUID REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    retrieved_at TIMESTAMP DEFAULT NOW(),
    relevance_score FLOAT,
    was_referenced BOOLEAN DEFAULT FALSE,
    user_feedback INTEGER CHECK (user_feedback BETWEEN 1 AND 5),
    metadata JSONB
);

CREATE INDEX idx_kb_analytics_document ON knowledge_base_analytics(document_id);
CREATE INDEX idx_kb_analytics_conversation ON knowledge_base_analytics(conversation_id);
CREATE INDEX idx_kb_analytics_timestamp ON knowledge_base_analytics(retrieved_at);
"""
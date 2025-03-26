create_table_sql_query = """
CREATE TABLE conversations (
    conversation_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    conversation_title TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    feedback TEXT,
    intervention_required BOOLEAN DEFAULT FALSE,
    topic TEXT
);

CREATE TABLE messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    sender VARCHAR(10) CHECK (sender IN ('user', 'bot')),
    text TEXT NOT NULL,
    is_useful BOOLEAN, -- For Thumbs up Thumbs down
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION fetch_conversation_stats_json(
    start_date TIMESTAMP,
    end_date TIMESTAMP
)
RETURNS JSON
LANGUAGE plpgsql
AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'total_conversations', (
            SELECT COUNT(*) 
            FROM conversations 
            WHERE created_at BETWEEN start_date AND end_date
        ),
        'avg_messages_per_conversation', (
            SELECT ROUND(AVG(msg_count), 2)
            FROM (
                SELECT COUNT(*) AS msg_count
                FROM messages
                WHERE created_at BETWEEN start_date AND end_date
                GROUP BY conversation_id
            ) AS msg_counts
        ),
        'total_users', (
            SELECT COUNT(DISTINCT user_id)
            FROM conversations
            WHERE created_at BETWEEN start_date AND end_date
        ),
        'intervention_count', (
            SELECT COUNT(*) 
            FROM conversations
            WHERE intervention_required = TRUE AND created_at BETWEEN start_date AND end_date
        ),
        'avg_time_spent_per_conversation_seconds', (
            SELECT ROUND(EXTRACT(EPOCH FROM AVG(duration))::numeric, 2)
            FROM (
                SELECT MAX(created_at) - MIN(created_at) AS duration
                FROM messages
                WHERE created_at BETWEEN start_date AND end_date
                GROUP BY conversation_id
            ) AS durations
        ),
        'avg_rating', (
            SELECT ROUND(AVG(rating), 2)
            FROM conversations
            WHERE rating IS NOT NULL AND created_at BETWEEN start_date AND end_date
        ),
        'new_users_since_start', (
            SELECT COUNT(DISTINCT user_id)
            FROM conversations c
            WHERE created_at BETWEEN start_date AND end_date
            AND NOT EXISTS (
                SELECT 1 FROM conversations c_prev
                WHERE c_prev.user_id = c.user_id
                AND c_prev.created_at < start_date
            )
        ),
        'top_topics', (
            SELECT json_agg(t)
            FROM (
                SELECT topic, COUNT(*) AS frequency
                FROM conversations
                WHERE created_at BETWEEN start_date AND end_date
                GROUP BY topic
                ORDER BY frequency DESC
                LIMIT 10
            ) AS t
        ),
        'user_queries_over_time', (
            SELECT json_agg(q)
            FROM (
                SELECT DATE_TRUNC('day', created_at) AS date, COUNT(*) AS total
                FROM messages
                WHERE sender = 'user' AND created_at BETWEEN start_date AND end_date
                GROUP BY date
                ORDER BY date
            ) AS q
        ),
        'top_unresolved_topics', (
            SELECT json_agg(u)
            FROM (
                SELECT topic, COUNT(*) AS unresolved_count
                FROM conversations
                WHERE intervention_required = TRUE AND created_at BETWEEN start_date AND end_date
                GROUP BY topic
                ORDER BY unresolved_count DESC
                LIMIT 10
            ) AS u
        ),
        'user_experience_over_time', (
            SELECT json_agg(r)
            FROM (
                SELECT DATE_TRUNC('day', updated_at) AS date, ROUND(AVG(rating), 2) AS avg_rating
                FROM conversations
                WHERE rating IS NOT NULL AND created_at BETWEEN start_date AND end_date
                GROUP BY date
                ORDER BY date
            ) AS r
        )
    ) INTO result;

    RETURN result;
END;
$$;

"""
"""
If you do not have Supabase already set up,
This module contains SQL queries and functions that need to be executed in the Supabase SQL Editor.

Instructions:
1. Open the Supabase Dashboard and navigate to your project.
2. Go to the "SQL Editor" section in the dashboard.
3. Copy the SQL script from this file below and paste it into the SQL Editor.
4. Click "Run" to execute the script and create the necessary tables and functions.

Note: Verify the changes in the "Table Editor" and "Functions" sections after execution.
"""

SUPABASE_DB_SQL_QUERY_SETUP = """
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
                SELECT d::DATE AS date, COALESCE(COUNT(m.message_id), 0) AS total
                FROM generate_series(start_date::DATE, end_date::DATE, '1 day') d
                LEFT JOIN messages m ON DATE_TRUNC('day', m.created_at) = d AND m.sender = 'user'
                GROUP BY d
                ORDER BY d
            ) AS q
        ),
        'top_unresolved_topics', (
            SELECT json_agg(u)
            FROM (
                SELECT 
                    u.faculty,
                    c.topic, 
                    COUNT(*) AS unresolved_count
                FROM conversations c
                JOIN users u ON c.user_id = u.user_id
                WHERE c.intervention_required = TRUE
                  AND c.created_at BETWEEN start_date AND end_date
                GROUP BY u.faculty, c.topic
                ORDER BY unresolved_count DESC
                LIMIT 10
            ) AS u
        ),
        'user_experience_over_time', (
            SELECT json_agg(r)
            FROM (
                SELECT d::DATE AS date, ROUND(AVG(c.rating), 2) AS avg_rating
                FROM generate_series(start_date::DATE, end_date::DATE, '1 day') d
                LEFT JOIN conversations c 
                    ON DATE_TRUNC('day', c.updated_at) = d 
                    AND c.rating IS NOT NULL 
                    AND c.created_at BETWEEN start_date AND end_date
                GROUP BY d
                ORDER BY d
            ) AS r
        ),
        'total_feedbacks', (
            SELECT COUNT(*)
            FROM conversations
            WHERE feedback IS NOT NULL AND created_at BETWEEN start_date AND end_date
        ),
        'total_thumbs_up', (
            SELECT COUNT(*)
            FROM messages
            WHERE is_useful = TRUE AND created_at BETWEEN start_date AND end_date
        ),
        'total_thumbs_down', (
            SELECT COUNT(*)
            FROM messages
            WHERE is_useful = FALSE AND created_at BETWEEN start_date AND end_date
        ),
        'recent_feedbacks', (
            SELECT json_agg(f)
            FROM (
                SELECT conversation_id, user_id, feedback, created_at
                FROM conversations
                WHERE feedback IS NOT NULL AND created_at BETWEEN start_date AND end_date
                ORDER BY created_at DESC
                LIMIT 5
            ) AS f
        ),
        'recent_thumbs_up_messages', (
            SELECT json_agg(m)
            FROM (
                SELECT message_id, conversation_id, sender, text, created_at
                FROM messages
                WHERE is_useful = TRUE AND created_at BETWEEN start_date AND end_date
                ORDER BY created_at DESC
                LIMIT 5
            ) AS m
        ),
        'recent_thumbs_down_messages', (
            SELECT json_agg(m)
            FROM (
                SELECT message_id, conversation_id, sender, text, created_at
                FROM messages
                WHERE is_useful = FALSE AND created_at BETWEEN start_date AND end_date
                ORDER BY created_at DESC
                LIMIT 5
            ) AS m
        )
    ) INTO result;

    RETURN result;
END;
$$;
"""
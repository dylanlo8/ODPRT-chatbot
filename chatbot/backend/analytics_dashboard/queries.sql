-- Define date range
-- Start: '2024-01-01 00:00:00'
-- End:   '2025-12-31 23:59:59'

--  Conversations Created
SELECT 
    COUNT(*) AS total_conversations
FROM 
    conversations
WHERE created_at BETWEEN '2024-01-01 00:00:00' AND '2025-12-31 23:59:59';

-- Average Number of Messages per Conversation
SELECT 
    AVG(msg_count) AS avg_messages_per_convo
FROM (
    SELECT COUNT(*) AS msg_count
    FROM messages
    WHERE created_at BETWEEN '2024-01-01 00:00:00' AND '2025-12-31 23:59:59'
    GROUP BY conversation_id
) AS message_counts;

-- Total Users (based on user_id)
SELECT 
    COUNT(DISTINCT user_id) AS total_users
FROM conversations
WHERE created_at BETWEEN '2024-01-01 00:00:00' AND '2025-12-31 23:59:59';

-- Intervention Count
SELECT 
    COUNT(intervention_required) AS intervention_count
FROM conversations
WHERE 
    created_at BETWEEN '2024-01-01 00:00:00' AND '2025-12-31 23:59:59'
    AND intervention_required = TRUE;

-- Average Time Spent per Conversation
SELECT 
    AVG(duration) AS avg_time_spent
FROM (
    SELECT MAX(created_at) - MIN(created_at) AS duration
    FROM messages
    WHERE created_at BETWEEN '2024-01-01 00:00:00' AND '2025-12-31 23:59:59'
    GROUP BY conversation_id
) AS convo_durations;

-- Average Rating per Conversation
SELECT 
    ROUND(AVG(rating), 2) AS avg_rating
FROM conversations
WHERE created_at BETWEEN '2024-01-01 00:00:00' AND '2025-12-31 23:59:59'
  AND rating IS NOT NULL;

-- New Users (unique user_ids)
SELECT 
    COUNT(DISTINCT user_id) AS new_users
FROM conversations c
WHERE created_at BETWEEN '2025-03-27 00:00:00' AND '2025-12-31 23:59:59'
  AND NOT EXISTS (
    SELECT 1
    FROM conversations c_prev
    WHERE c_prev.user_id = c.user_id
      AND c_prev.created_at < '2025-03-27 00:00:00'
);

-- =======================
-- MIDDLE SECTION - CHARTS
-- =======================

-- Top 10 Most Common Conversation Topics
SELECT 
    topic, 
    COUNT(*) AS frequency
FROM conversations
WHERE sender = 'user'
  AND created_at BETWEEN '2024-01-01 00:00:00' AND '2025-12-31 23:59:59'
GROUP BY topic
ORDER BY frequency DESC
LIMIT 10;

-- User Queries Over Time
SELECT
  DATE_TRUNC('day', created_at) AS query_date,
  COUNT(*) AS total_queries
FROM messages
WHERE sender = 'user'
  AND created_at BETWEEN '2024-01-01 00:00:00' AND '2025-12-31 23:59:59'
GROUP BY query_date
ORDER BY query_date;


-- =======================
-- BOTTOM SECTION - DEEPER ANALYSIS
-- =======================

-- Top 10 Most Common Unresolved Queries
SELECT 
    topic, 
    COUNT(*) AS unresolved_count
FROM conversations
WHERE intervention_required = TRUE
  AND created_at BETWEEN '2024-01-01 00:00:00' AND '2025-12-31 23:59:59'
GROUP BY topic
ORDER BY unresolved_count DESC
LIMIT 10;

-- User Experience Over Time
SELECT 
    DATE_TRUNC('day', updated_at) AS rating_date, 
    ROUND(AVG(rating), 2) AS avg_rating
FROM conversations
WHERE rating IS NOT NULL
  AND created_at BETWEEN '2024-01-01 00:00:00' AND '2025-12-31 23:59:59'
GROUP BY rating_date
ORDER BY rating_date;

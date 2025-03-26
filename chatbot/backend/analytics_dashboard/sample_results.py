# Running SELECT fetch_conversation_stats_json('2024-01-01', '2025-12-31');
SAMPLE_RESULT = {
  "total_conversations": 3,
  "avg_messages_per_conversation": 2,
  "total_users": 1,
  "intervention_count": 1,
  "avg_time_spent_per_conversation_seconds": 115205.62,
  "avg_rating": 5,
  "new_users_since_start": 1,
  "top_topics": [
    {
      "topic": "IEP",
      "frequency": 3
    }
  ],
  "user_queries_over_time": [
    {
      "date": "2025-03-24T00:00:00",
      "total": 1
    },
    {
      "date": "2025-03-26T00:00:00",
      "total": 3
    }
  ],
  "top_unresolved_topics": [
    {
      "topic": "IEP",
      "unresolved_count": 1
    }
  ],
  "user_experience_over_time": [
    {
      "date": "2025-03-24T00:00:00",
      "avg_rating": 5
    }
  ]
}


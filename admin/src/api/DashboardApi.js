import axios from "axios";

const BASE_URL = "http://localhost:8000";

export const fetchDashboardData = async (range) => {
  try {
    const response = await axios.post(`${BASE_URL}/dashboard/fetch`, {
      start_date: String(range.from),
      end_date: String(range.to),
    });
    return response.data; // Return the fetched data
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
    throw error; // Re-throw the error for handling in the calling component
  }
};

/**
 * Sample Response Format:
 * 
 * {
 *   "total_conversations": 13,
 *   "avg_messages_per_conversation": 1.46,
 *   "total_users": 2,
 *   "intervention_count": 2,
 *   "avg_time_spent_per_conversation_seconds": 26587.16,
 *   "avg_rating": 5,
 *   "new_users_since_start": 2,
 *   "top_topics": [
 *     { "topic": null, "frequency": 5 },
 *     { "topic": "null", "frequency": 4 },
 *     { "topic": "IEP", "frequency": 2 },
 *     { "topic": "IEP Contracting Hub Usage", "frequency": 1 },
 *     { "topic": "Grant Progress Reporting", "frequency": 1 }
 *   ],
 *   "user_queries_over_time": [
 *     { "date": "2025-03-24T00:00:00", "total": 1 },
 *     { "date": "2025-03-26T00:00:00", "total": 3 },
 *     { "date": "2025-03-27T00:00:00", "total": 1 },
 *     { "date": "2025-04-01T00:00:00", "total": 7 },
 *     { "date": "2025-04-02T00:00:00", "total": 2 }
 *   ],
 *   "top_unresolved_topics": [
 *     { "topic": "Grant Progress Reporting", "unresolved_count": 1 },
 *     { "topic": "IEP", "unresolved_count": 1 }
 *   ],
 *   "user_experience_over_time": [
 *     { "date": "2025-03-24T00:00:00", "avg_rating": 5 },
 *     { "date": "2025-03-26T00:00:00", "avg_rating": 5 }
 *   ],
 *   "total_feedbacks": 1,
 *   "total_thumbs_up": 1,
 *   "total_thumbs_down": 1,
 *   "recent_feedbacks": [
 *     {
 *       "conversation_id": "b2397379-5ab3-47eb-815e-f92910145e01",
 *       "user_id": "5da3e33e-37ff-489f-be64-fc5e76f17c1e",
 *       "feedback": "test",
 *       "created_at": "2025-03-26T05:51:02.33782"
 *     }
 *   ],
 *   "recent_thumbs_up_messages": [
 *     {
 *       "message_id": "b3c82975-763a-4ccf-84c4-245e42437c76",
 *       "conversation_id": "b45d8d8d-05c3-4cc8-9307-79307c6d1d0c",
 *       "sender": "bot",
 *       "text": "To make ODPRT Contracting Agreements, you can use the IEP Contracting Hub hosted in ODPRT...",
 *       "created_at": "2025-03-27T10:06:01.957848"
 *     }
 *   ],
 *   "recent_thumbs_down_messages": [
 *     {
 *       "message_id": "dd2e40d0-8229-4f22-96af-277b31124cb3",
 *       "conversation_id": "b2397379-5ab3-47eb-815e-f92910145e01",
 *       "sender": "bot",
 *       "text": "To apply for ODPRT research-related grants, follow these steps...",
 *       "created_at": "2025-03-26T05:51:10.319973"
 *     }
 *   ]
 * }
 */
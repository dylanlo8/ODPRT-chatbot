export const mockResponses = {
    fetchUserConversations: [
      {
        conversation_id: "123e4567-e89b-12d3-a456-426614174000",
        user_id: "123e4567-e89b-12d3-a456-426614174000",
        conversation_title: "Sample Conversation",
        created_at: "2025-03-15T08:29:52.996305",
        updated_at: "2025-03-15T08:29:52.996305",
        rating: null,
        feedback: null,
      },
      {
        conversation_id: "helllo1110",
        user_id: "123e4567-e89b-12d3-a456-426614174000",
        conversation_title: "Sample Conversation",
        created_at: "2025-03-15T08:29:52.996305",
        updated_at: "2025-03-15T08:29:52.996305",
        rating: null,
        feedback: null,
      },
    ],
    fetchConversationMessages: [
      {
        message_id: "58298043-8f70-410b-982d-9ffa58bdb092",
        conversation_id: "123e4567-e89b-12d3-a456-426614174000",
        sender: "Human",
        text: "Hello, how can I help you thanks?",
        is_useful: null,
        created_at: "2025-03-15T08:29:53.163697",
      },
      {
        message_id: "58298043-8f70-410b-982d-9ffa58bdb092",
        conversation_id: "123e4567-e89b-12d3-a456-426614174000",
        sender: "AI",
        text: "AI reply",
        is_useful: null,
        created_at: "2025-03-15T08:29:53.163697",
      },
    ],
  };
  
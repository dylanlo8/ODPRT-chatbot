from chatbot.backend.chains.query_chains import answer_chain, routing_chain

def semantic_router(user_query) -> str: 
    result = routing_chain.invoke({"user_query": user_query})
    classification = result["classification"]
    
    if classification == "VAGUE": 
        return "Your question is unclear. Can you provide more details?"
    
    elif classification == "NOT_RELATED":
        return "I am unable to help with that topic."
    
    elif classification == "RELATED":
        return generate_answer(user_query)
    
def generate_answer(user_query) -> str: 
    return answer_chain.invoke({"user_query": user_query})

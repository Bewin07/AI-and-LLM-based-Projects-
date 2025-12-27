from embedder import embed_User_query
from vectorstore import search_in_pinecone
from llm import query_llm_with_context

def process_user_query(query: str):
    # Embed the user's query to create a vector representation
    query_vector = embed_User_query(query)
    
    # Search the vector DB to find top matching chunks related to the user's question
    matched_chunks_context = search_in_pinecone(query_vector, top_k=3)
    
    # Send the user query and the search results (query + context) to the LLM for Generating response
    bot_response = query_llm_with_context(query, matched_chunks_context)
    return bot_response, matched_chunks_context

if __name__ == "__main__":
    user_query = "What is this document about?"
    # Simple test
    try:
        response, context = process_user_query(user_query)
        print("Bot Response:", response)
    except Exception as e:
        print(f"Error: {e}")
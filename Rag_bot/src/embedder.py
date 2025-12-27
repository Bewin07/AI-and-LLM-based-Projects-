import google.generativeai as genai
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def embed_chunks(chunks: List[str], model: str = "models/text-embedding-004") -> List[List[float]]:
    """
    Embeds the list of text chunks using Gemini's embedding model.
    """

    embeddings = []
    for chunk in chunks:
        response = genai.embed_content(
            model=model,
            content=chunk
        )
        embedding = response["embedding"]
        embeddings.append(embedding)

    return embeddings

def embed_User_query(query: str, model: str = "models/text-embedding-004") -> List[float]:
    """
    Embeds a single query string.
    """
    response = genai.embed_content(
        model=model,
        content=query
    )
    return response["embedding"]

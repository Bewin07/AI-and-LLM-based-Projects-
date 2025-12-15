"""
generator.py — AI Keyword Generator using Groq Llama API
Author: KeywordIQ Team
"""

import os
from groq import Groq

from dotenv import load_dotenv

load_dotenv()

gapi_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client (ensure GROQ_API_KEY is set in environment)
client = Groq(api_key=gapi_key)

def get_ai_suggestions(keywords, n_keywords=20):
    """
    Generate semantically similar or long-tail keywords using Llama.
    """
    if not keywords:
        return ["No keywords provided"]

    # Limit to first 20 base keywords to keep prompt concise
    base_keywords = ", ".join(keywords[:20])

    prompt = f"""
    You are an SEO keyword research assistant.
    Generate {n_keywords} semantically related and long-tail keywords 
    based on the following seed keywords:

    {base_keywords}

    Return only the keywords as a plain bullet list.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content
        # Clean and return as list
        lines = [line.strip("-• ") for line in content.splitlines() if line.strip()]
        return lines
    except Exception as e:
        print(f"❌ Groq API Error: {e}")
        return [f"Error: {e}"]

def summarize_keyword_themes(keywords):
    """
    Summarize main topics and keyword clusters for analytics insights.
    """
    if not keywords:
        return "No keywords available for summary."

    prompt = f"""
    Analyze and summarize the following keywords into thematic clusters.
    Mention the top 3-5 main themes or industries they relate to.

    Keywords:
    {', '.join(keywords[:50])}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error summarizing keywords: {e}"

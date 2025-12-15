import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
from google.api_core.exceptions import ResourceExhausted
from functools import lru_cache

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Step 4: Use a cheaper / higher-limit model (Gemini 1.5 Flash -> gemini-flash-latest)
model = genai.GenerativeModel('models/gemini-flash-latest')

# Step 5: Cache responses
@lru_cache(maxsize=100)
def query_llm_with_context(query: str, context: str) -> str:
    # Step 3: Add a HARD token guardrail (Truncate context)
    MAX_CONTEXT_CHARS = 3000
    if len(context) > MAX_CONTEXT_CHARS:
        context = context[:MAX_CONTEXT_CHARS]

    # Step 6: Smart prompt (short + strict)
    system_instruction = """Answer the question using ONLY the given context.
If the answer is not found, say "Not available in document".
"""

    prompt = f"{system_instruction}\n\nContext:\n{context}\n\nQuestion:\n{query}"
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except ResourceExhausted:
            wait_time = (2 ** attempt) * 5  # 5s, 10s, 20s
            print(f"Quota exceeded. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except Exception as e:
            if "429" in str(e):
                wait_time = (2 ** attempt) * 5
                print(f"Quota exceeded (429). Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e
    
    return "I apologize, but I am currently experiencing high traffic (Rate Limit Exceeded). Please try again in a minute."

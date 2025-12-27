import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

models = list(genai.list_models())
with open("models.txt", "w") as f:
    for m in models:
        f.write(f"{m.name}\n")
        f.write(f"Methods: {m.supported_generation_methods}\n")
        f.write("-" * 20 + "\n")

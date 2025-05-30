import json
import openai
import os
from tqdm import tqdm
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # ✅ Load environment variables from .env
print("API Key:", os.getenv("OPENAI_API_KEY"))  # Just for debugging

# Load OpenAI API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load Quran data
with open('quran.json', 'r', encoding='utf-8') as f:
    verses = json.load(f)

# ✅ TEMPORARY FIX: Only embed the first 10 verses
verses = verses[:10]

# Add embedding field
for verse in tqdm(verses, desc="Generating embeddings"):
    try:
        response = client.embeddings.create(
            input=verse['english'],
            model='text-embedding-ada-002'
        )
        verse['embedding'] = response.data[0].embedding
    except Exception as e:
        print(f"Failed to generate embedding for verse {verse['surah']}:{verse['ayah']} - {e}")
        verse['embedding'] = None

# Save the result
with open('quran_with_embeddings.json', 'w', encoding='utf-8') as f:
    json.dump(verses, f, ensure_ascii=False, indent=2)

print("✅ Embeddings generated and saved.")

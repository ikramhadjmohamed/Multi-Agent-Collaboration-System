import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # reads .env and loads GROQ_API_KEY into the environment

api_key = os.getenv("GROQ_API_KEY")
print("Key loaded:", bool(api_key))  # sanity check — should print True, not the key itself

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Reply with exactly one word: OK"}],
    max_tokens=10,
)

print(response.choices[0].message.content)
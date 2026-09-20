from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("API KEY:", "FOUND" if api_key else "NOT FOUND")

client = genai.Client(api_key=api_key)

print("Sending test request...")

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Say hello in one sentence."
)

print("\nGemini response:")
print(response.text)
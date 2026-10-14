
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Explain what a software version is in two sentences."
    )

    print("Gemini response:")
    print(response.text)

except Exception as error:
    print("Gemini request failed:")
    print(error)

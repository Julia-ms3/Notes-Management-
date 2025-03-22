# SET UP GEMINI
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))


def summarize_text(text):
    content = f'please summarize the following text:\n\n{text}'
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[content])

    return response.text

from dotenv import load_dotenv
from openai import OpenAI
from os import getenv

class OpenAIService:
    def __init__(self):
        load_dotenv()
        self.client = client = OpenAI(api_key=getenv("OPENAI_API_KEY"))

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "",
                },
                {
                    "role": "user",
                    "content": "Say this is a test",
                }
            ],
            model="gpt-3.5-turbo",
        )
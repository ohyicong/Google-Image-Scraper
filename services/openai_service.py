import logging

from dotenv import load_dotenv
from openai import OpenAI
from os import getenv


class OpenAIService:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=getenv("OPENAI_API_KEY"))

    def get_product_description(self, product: str, website_content: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Estás encargado de buscar descripciones cortas e informativas sobre productos en línea. Vas a recibir el nombre de un producto, ademas del texto que incluye una página web con información sobre el mismo, y tu trabajo es devolver una descripción de máximo 256 palábras sobre el producto.",
                },
                {
                    "role": "user",
                    "content": "Producto: {}\n{}".format(product, website_content),
                },
            ],
            model="gpt-4o-mini",
        )
        return chat_completion.choices[0].message.content

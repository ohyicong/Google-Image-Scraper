import logging

from dotenv import load_dotenv
from openai import OpenAI
from os import getenv

from yaab.gpt_models.models import GPTDescriptionResponse


class OpenAIService:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=getenv("OPENAI_API_KEY"))

    def get_product_description(
        self, product: str, website_content: str
    ) -> GPTDescriptionResponse:
        """
        This gets a product's description by analyzing the webpage, and also attempts to find product dimensions.
        :param product:
        :param website_content:
        :return:
        """
        chat_completion = self.client.beta.chat.completions.parse(
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
            response_format=GPTDescriptionResponse,
        )
        try:
            return chat_completion.choices[0].message.parsed
        except Exception as e:
            print(chat_completion.choices)
            raise Exception("error on chatgpt parsed output")

import decimal
import os
from typing import List, Optional

import requests
from pydantic import BaseModel
from dotenv import load_dotenv

from yaab.api_models.models import Category, ExtraField, Variante, Producto


class YaabProduct(BaseModel):
    sku: str
    name: str
    category: str
    min_price: decimal.Decimal
    price: decimal.Decimal
    stock: int
    status: str
    description: str
    colors: List[str]
    ai_description: Optional[str] = None


class YaabStoreService:
    base_url = "https://dev.yaab.solutionslion.com/api"

    def __init__(self):
        load_dotenv()
        self.username = os.getenv("YAAB_USERNAME")
        self.password = os.getenv("YAAB_PASSWORD")

    def login(self):
        req_data = {
            "username": self.username,
            "password": self.password,
            "set_cookies": False,
        }
        url = self.base_url + "/login"

        res = requests.post(url, json=req_data)

    def get_extra_fields(self):
        url = self.base_url + "/campos-extras"
        res = requests.get(url)
        data = res.json()
        categories: List[ExtraField] = []
        for field in data:
            categories.append(ExtraField(**field))
        return categories

    def get_categories(self) -> List[Category]:
        url = self.base_url + "/productos"
        data = {"categoria"}
        res = requests.post(url)
        data = res.json()
        categories: List[Category] = []
        for cat in data:
            categories.append(Category(**cat))
        return categories

    def create_product(self, product: YaabProduct):
        url = self.base_url + "/categorias"

        mock_producto = Producto(
            categoria=1,
            descripcion="Producto de prueba",
            detalles="Detalles adicionales del producto",
            nombre="Producto Test",
            referencia="test123",
            variantes=[
                Variante(
                    sku="123456",
                    precio_proveedor=99.99,
                    campos_extras={"Color": "rojo", "Tamaño": "M"},
                    descuento=10.0,
                    alto=100,
                    largo=50,
                    ancho=30,
                    peso=5,
                ),
                Variante(
                    sku="789012",
                    precio_proveedor=79.99,
                    campos_extras={"Color": "azul"},
                    descuento=5.0,
                    alto=120,
                    largo=60,
                    ancho=40,
                    peso=7,
                ),
            ],
        )
        # todo test
        res = requests.post(url, json=mock_producto.model_dump_json())
        data = res.json()

        return data  # todo parse into pydantic response object, need api for this

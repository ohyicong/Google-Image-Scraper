from typing import Dict, List

from pydantic import BaseModel


class Category(BaseModel):
    id: int
    nombre: str
    imagen: str


class ExtraField(BaseModel):
    id: int
    nombre: str
    categoria: int


class Variante(BaseModel):
    sku: str
    precio_proveedor: float
    campos_extras: Dict[str, str]
    descuento: float
    alto: int
    largo: int
    ancho: int
    peso: int


class Producto(BaseModel):
    categoria: int
    descripcion: str
    detalles: str
    nombre: str
    referencia: str
    variantes: List[Variante]

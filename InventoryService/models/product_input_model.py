from dataclasses import dataclass

@dataclass
class ProductInputModel:
    merchant_id: int
    product_name: str
    price: float
    quantity: int

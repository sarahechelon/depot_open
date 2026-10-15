"""Product business logic. Must not import FastAPI."""

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductError(Exception):
    """Base class for product domain errors."""


class DuplicateSkuError(ProductError):
    def __init__(self, sku: str) -> None:
        super().__init__(f"product with sku {sku!r} already exists")
        self.sku = sku


class NotFoundError(ProductError):
    def __init__(self, sku: str) -> None:
        super().__init__(f"product with sku {sku!r} not found")
        self.sku = sku


def _get_by_sku(session: Session, sku: str) -> Product | None:
    return session.scalar(select(Product).where(Product.sku == sku))


def create_product(
    session: Session, sku: str, name: str, price: Decimal, stock_qty: int
) -> Product:
    if _get_by_sku(session, sku) is not None:
        raise DuplicateSkuError(sku)
    product = Product(sku=sku, name=name, price=price, stock_qty=stock_qty)
    session.add(product)
    session.flush()
    return product


def list_products(session: Session) -> list[Product]:
    return list(session.scalars(select(Product).order_by(Product.sku)))


def get_product(session: Session, sku: str) -> Product:
    product = _get_by_sku(session, sku)
    if product is None:
        raise NotFoundError(sku)
    return product


def update_product(
    session: Session,
    sku: str,
    name: str | None = None,
    price: Decimal | None = None,
    stock_qty: int | None = None,
) -> Product:
    product = get_product(session, sku)
    if name is not None:
        product.name = name
    if price is not None:
        product.price = price
    if stock_qty is not None:
        product.stock_qty = stock_qty
    session.flush()
    return product


def delete_product(session: Session, sku: str) -> None:
    product = get_product(session, sku)
    session.delete(product)
    session.flush()

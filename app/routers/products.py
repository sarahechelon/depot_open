from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db import get_session
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services import product as product_service

router = APIRouter(prefix="/products", tags=["products"])

DbSession = Annotated[Session, Depends(get_session)]


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(body: ProductCreate, session: DbSession) -> ProductRead:
    try:
        created = product_service.create_product(
            session, body.sku, body.name, body.price, body.stock_qty
        )
    except product_service.DuplicateSkuError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return ProductRead.model_validate(created)


@router.get("", response_model=list[ProductRead])
def list_products(session: DbSession) -> list[ProductRead]:
    return [ProductRead.model_validate(p) for p in product_service.list_products(session)]


@router.get("/{sku}", response_model=ProductRead)
def get_product(sku: str, session: DbSession) -> ProductRead:
    try:
        found = product_service.get_product(session, sku)
    except product_service.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ProductRead.model_validate(found)


@router.patch("/{sku}", response_model=ProductRead)
def update_product(sku: str, body: ProductUpdate, session: DbSession) -> ProductRead:
    try:
        updated = product_service.update_product(
            session, sku, name=body.name, price=body.price, stock_qty=body.stock_qty
        )
    except product_service.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ProductRead.model_validate(updated)


@router.delete("/{sku}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(sku: str, session: DbSession) -> Response:
    try:
        product_service.delete_product(session, sku)
    except product_service.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)

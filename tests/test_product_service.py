import pytest
from pydantic_settings import BaseSettings
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.models.productdb import ProductEntity
from app.services.productservice import ProductService


def test_product_enable():
    # Arrange
    repository = MagicMock()

    product = ProductEntity(
        id=1,
        tenant_id=10,
        name="Laptop",
        active=False,
    )

    repository.first.return_value = product

    service = ProductService(repository)

    # Act
    result = service.product_enable_disable(
        id=1,
        active=True,
        tenant_id=10,
    )

    # Assert
    assert result is product
    assert result.active is True

    repository.first.assert_called_once()

import uuid

from django.shortcuts import get_object_or_404
from ninja import Router

from project.api.product import models, schemas

router = Router(tags=["product"])


@router.get("/logs", response=list[schemas.ProductLogResponse])
def list_product_logs(request):
    return models.ProductLog.objects.all()


@router.get("/search", response=list[schemas.ProductResponse])
def search_product(request, query: str): ...


@router.get("", response=list[schemas.ProductResponse])
def list_products(request):
    return models.Product.objects.all()


@router.post("", response=schemas.ProductResponse)
def create_product(request, product: schemas.ProductCreate):
    product = models.Product(**product.dict())
    product.full_clean()
    product.save()

    return product


@router.get("/{product_id}", response=schemas.ProductResponse)
def get_product(request, product_id: uuid.UUID):
    return get_object_or_404(models.Product, id=product_id)


@router.put("/{product_id}", response=schemas.ProductResponse)
def update_product(
    request,
    product_id: uuid.UUID,
    product: schemas.ProductCreate,
):
    product_model = get_object_or_404(models.Product, id=product_id)
    for attr, value in product.dict().items():
        setattr(product_model, attr, value)
    product_model.save()

    return product_model


@router.delete("/{product_id}")
def delete_product(request, product_id: uuid.UUID):
    product = get_object_or_404(models.Product, id=product_id)
    product.delete()

    return {"success": True}

import datetime
import uuid
from collections import defaultdict
from datetime import timedelta
from http import HTTPStatus as status

from django.db.models import F
from django.db.models.manager import BaseManager
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import Router

from api.v1.product import schemas
from apps.product.log.models import ProductLog
from apps.product.models import Product

router = Router(tags=["product"])


@router.get(
    "/notifications", response={status.OK: list[schemas.NotificationOut]}
)
def get_notifications(
    request: HttpRequest,
) -> tuple[int, list[schemas.NotificationOut]]:
    today = timezone.now().date()
    threshold_date = today + timedelta(days=3)

    products = Product.objects.filter(expiration_date__lte=threshold_date)

    notifications = []
    for product in products:
        exp_date = product.expiration_date

        if exp_date <= today:
            notifications.append(
                schemas.NotificationOut(
                    name=product.name,
                    level="critical",
                    type="product_expiry",
                    timestamp=datetime.datetime(
                        exp_date.year,
                        exp_date.month,
                        exp_date.day,
                        tzinfo=datetime.UTC,
                    ),
                )
            )
        if exp_date - timedelta(days=1) <= today:
            notifications.append(
                schemas.NotificationOut(
                    name=product.name,
                    level="high",
                    type="product_expiry",
                    timestamp=datetime.datetime(
                        exp_date.year,
                        exp_date.month,
                        exp_date.day,
                        tzinfo=datetime.UTC,
                    )
                    - timedelta(days=1),
                )
            )
        if exp_date - timedelta(days=3) <= today:
            notifications.append(
                schemas.NotificationOut(
                    name=product.name,
                    level="average",
                    type="product_expiry",
                    timestamp=datetime.datetime(
                        exp_date.year,
                        exp_date.month,
                        exp_date.day,
                        tzinfo=datetime.UTC,
                    )
                    - timedelta(days=3),
                )
            )

    notifications.sort(key=lambda x: x.timestamp, reverse=True)

    return status.OK, notifications


@router.get("/categories", response=list[str])
def get_categories(request: HttpRequest) -> tuple[int, list[str]]:
    return status.OK, set(Product.objects.values_list("category", flat=True))


@router.get("/manufacturers", response=list[str])
def get_manufactorers(request: HttpRequest) -> tuple[int, list[str]]:
    return status.OK, set(
        Product.objects.values_list("manufacturer", flat=True)
    )


@router.get("/analytics", response=list[schemas.DailyChangeOut])
def get_products_stats(
    request: HttpRequest,
    date_after: datetime.date,
    date_before: datetime.date,
) -> tuple[int, list[schemas.DailyChangeOut]]:
    entries = ProductLog.objects.filter(
        timestamp__date__range=(date_after, date_before)
    )
    positive_daily_change = defaultdict(float)
    negative_daily_change = defaultdict(float)

    for entry in entries:
        day = entry.timestamp.date()

        if entry.quantity_change >= 0:
            positive_daily_change[day] += entry.quantity_change
        else:
            negative_daily_change[day] -= entry.quantity_change

    delta = datetime.timedelta(days=1)
    daily_changes = []
    day = date_after

    while day <= date_before:
        daily_changes.append(
            schemas.DailyChangeOut(
                date=day,
                positive_quantity_change_for_date=positive_daily_change[day],
                negative_quantity_change_for_date=negative_daily_change[day],
            )
        )
        day += delta

    return status.OK, daily_changes


@router.post("/search_by_qr", response=list[schemas.ProductOut])
def search_product_by_qr(
    request: HttpRequest, product: schemas.SearchProductIn
) -> tuple[int, BaseManager[Product]]:
    return status.OK, Product.objects.filter(
        **product.dict(exclude_unset=True)
    )


@router.get("", response=list[schemas.ProductOut])
def list_products(request: HttpRequest) -> tuple[int, BaseManager[Product]]:
    return status.OK, Product.objects.order_by(F("timestamp").desc())


@router.post("", response={status.CREATED: schemas.ProductOut})
def create_product(
    request: HttpRequest, product: schemas.ProductIn
) -> tuple[int, Product]:
    product_obj = Product(**product.dict())
    product_obj.full_clean()
    product_obj.save()

    return status.CREATED, product_obj


@router.get("/{product_id}", response={status.OK: schemas.ProductOut})
def get_product(
    request: HttpRequest, product_id: uuid.UUID
) -> tuple[int, Product]:
    product = get_object_or_404(Product, id=product_id)

    return status.OK, product


@router.put("/{product_id}", response={status.OK: schemas.ProductOut})
def update_product(
    request: HttpRequest,
    product_id: uuid.UUID,
    product: schemas.ProductIn,
) -> tuple[int, Product]:
    product_obj = get_object_or_404(Product, id=product_id)

    for attr, value in product.dict().items():
        setattr(product_obj, attr, value)

    product_obj.full_clean()
    product_obj.save()

    return status.OK, product_obj


@router.delete(
    "/{product_id}",
    response={status.NO_CONTENT: None},
)
def delete_product(
    request: HttpRequest, product_id: uuid.UUID
) -> tuple[int, None]:
    product = get_object_or_404(Product, id=product_id)
    product.delete()

    return status.NO_CONTENT, None

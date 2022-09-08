from typing import List

from django.contrib.admin.views.decorators import staff_member_required
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from ninja import Header, NinjaAPI, Path
from ninja.pagination import paginate
from ninja.security import django_auth

from .decorator import has_perm
from .dto import ErrResponse, ItemRequest, ItemResponse, OrderRequest, OrderResponse, ValidateErrResponse
from .models import Item, Order

api = NinjaAPI(
    title="api",
    version="1.0.0",
    description="""Blueprint `api` exposes endpoints that alllow user manipulate items and orders""",
    csrf=True,
    auth=django_auth,
    docs_decorator=staff_member_required,
)


@api.get(
    "/item/{id}",
    tags=["items"],
    operation_id="view_item",
    response={200: ItemResponse, 403: ErrResponse, 422: ValidateErrResponse},
)
@has_perm("api.view_item")
def get_item(
    request: HttpRequest,
    id: int = Path(default=None, description=_("Item ID")),
    lang: str | None = Header(alias="accept-language", default=None),
):
    """
    Query an item by id
    """
    return 200, get_object_or_404(Item, id=id, delete_status=False)


@api.get(
    "/items",
    tags=["items"],
    operation_id="view_items",
    response={200: List[ItemResponse], 403: ErrResponse, 422: ValidateErrResponse},
)
@has_perm("api.view_item")
@paginate
def get_items(request: HttpRequest, lang: str | None = Header(alias="accept-language", default=None)):
    """
    Query items
    """
    return Item.objects.filter(delete_status=False).all()


@api.put(
    "/item", tags=["items"], operation_id="add_item", response={200: int, 403: ErrResponse, 422: ValidateErrResponse}
)
@has_perm("api.add_item")
def add_item(
    request: HttpRequest,
    payload: ItemRequest,
    lang: str | None = Header(alias="accept-language", default=None),
):
    """
    Create an item
    """
    item = Item.create(payload)
    return 200, item.id


@api.get(
    "/order/{id}",
    tags=["orders"],
    operation_id="view_order",
    response={200: OrderResponse, 403: ErrResponse, 422: ValidateErrResponse},
)
@has_perm("api.view_order")
def get_order(
    request: HttpRequest,
    id: int = Path(default=None, description=_("Order ID")),
    lang: str | None = Header(alias="accept-language", default=None),
):
    """
    Query an order by id
    """
    return 200, get_object_or_404(Order, id=id, delete_status=False)


@api.get(
    "/orders",
    tags=["orders"],
    operation_id="view_orders",
    response={200: List[OrderResponse], 403: ErrResponse, 422: ValidateErrResponse},
)
@has_perm("api.view_order")
@paginate
def get_orders(request: HttpRequest, lang: str | None = Header(alias="accept-language", default=None)):
    """
    Query orders
    """
    return Order.objects.filter(delete_status=False).all()


@api.put(
    "/order", tags=["orders"], operation_id="add_order", response={200: int, 403: ErrResponse, 422: ValidateErrResponse}
)
@has_perm("api.add_order")
def add_order(
    request: HttpRequest,
    payload: OrderRequest,
    lang: str | None = Header(alias="accept-language", default=None),
):
    """
    Place an order
    """
    order: Order = Order.buy(Order, payload.id, payload.quantity, payload.buy)
    return 200, order.id

from datetime import datetime

from django.db import models
from django.db.transaction import atomic
from django.db.utils import DataError
from django.utils.translation import gettext as _
from ninja import Schema
from ninja.errors import ValidationError
from typing_extensions import Self

# Create your models here.


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(_("Create time"), auto_now=True)
    update_time = models.DateTimeField(_("Update time"), auto_now_add=True)
    delete_status = models.BooleanField(_("Delete status"), null=False, default=False)

    @classmethod
    def create(cls, schema: Schema) -> Self:
        obj: Self = cls(**schema.dict(exclude={"id"}))
        obj.save()
        return obj

    class Meta:
        abstract = True


class Item(BaseModel):

    name = models.CharField(_("Item name"), null=False, max_length=255)
    stock = models.PositiveIntegerField(_("Item stock"), null=False, default=0)
    sold = models.PositiveBigIntegerField(_("Item sold"), null=False, default=0)
    last = models.DateTimeField(_("Item last sold time"), null=True)

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Item")

    def buy(self, quantity: int):
        if quantity <= 0:
            raise DataError(_("Error: quantity must large than 0"))
        self.stock = models.F("stock") - quantity
        self.sold = models.F("sold") + quantity
        self.last = datetime.now()
        self.save()


class Order(BaseModel):

    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, verbose_name=_("Item ID"))
    quantity = models.PositiveIntegerField(_("Item quantity"), null=False, default=0)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Order")

    @classmethod
    def create(cls, item: Item, quantity: int) -> Self:
        obj: Self = cls(item=item, quantity=quantity)
        obj.save()
        return obj

    @atomic
    def buy(self, id: int, quantity: int, buy: int) -> Self:
        item: Item | None = Item.objects.filter(pk=id).select_for_update().first()
        if not item:
            raise ValidationError(_("No such item"))
        if (item.sold + 1 != buy) | (quantity <= 0):
            raise ValidationError(_("Not valid order"))
        if item.stock < quantity:
            raise ValidationError(_("Not enough stock"))
        order = Order.create(item, quantity)
        order.save()
        item.buy(quantity)
        return order

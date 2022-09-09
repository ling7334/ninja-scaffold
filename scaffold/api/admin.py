from api import models
from django.contrib import admin


class ItemDisp(admin.ModelAdmin):
    list_display = ("id", "name", "stock", "sold", "last")
    list_filter = ("name", "stock", "sold", "last", "create_time", "update_time", "delete_status")


class OrderDisp(admin.ModelAdmin):
    list_display = ("id", "item", "quantity")
    list_filter = ("item__name", "quantity")


# Register your models here.
admin.site.register(models.Item, ItemDisp)
admin.site.register(models.Order, OrderDisp)

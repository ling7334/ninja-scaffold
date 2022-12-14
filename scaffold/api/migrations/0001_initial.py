# Generated by Django 4.1 on 2022-09-07 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "create_time",
                    models.DateTimeField(auto_now=True, verbose_name="Create time"),
                ),
                (
                    "update_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="Update time"),
                ),
                (
                    "delete_status",
                    models.BooleanField(default=False, verbose_name="Delete status"),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Item name")),
                (
                    "stock",
                    models.PositiveIntegerField(default=0, verbose_name="Item stock"),
                ),
                (
                    "sold",
                    models.PositiveBigIntegerField(default=0, verbose_name="Item sold"),
                ),
                (
                    "last",
                    models.DateTimeField(null=True, verbose_name="Item last sold time"),
                ),
            ],
            options={
                "verbose_name": "Item",
                "verbose_name_plural": "Item",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "create_time",
                    models.DateTimeField(auto_now=True, verbose_name="Create time"),
                ),
                (
                    "update_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="Update time"),
                ),
                (
                    "delete_status",
                    models.BooleanField(default=False, verbose_name="Delete status"),
                ),
                (
                    "quantity",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Item quantity"
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="api.item",
                        verbose_name="Item ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Order",
            },
        ),
    ]

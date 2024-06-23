# Generated by Django 3.2.18 on 2024-01-10 21:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0018_auto_20240110_2100"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartorder",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("process", "Processing"),
                    ("delivered", "Delivered"),
                    ("shipped", "Shipped"),
                ],
                default="Processing",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_character",
            field=models.CharField(
                choices=[("NEW", "new"), ("USED", "used")], default="new", max_length=10
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("published", "Published"),
                    ("disabled", "Disabled"),
                    ("rejected", "Rejected"),
                    ("in_review", "In Review"),
                    ("draft", "Draft"),
                ],
                default="in_review",
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="ProductInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("parametrs", models.TextField(blank=True, max_length=100, null=True)),
                (
                    "parameter_description",
                    models.TextField(blank=True, max_length=200, null=True),
                ),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_info",
                        to="core.product",
                    ),
                ),
            ],
        ),
    ]
# Generated by Django 3.2.18 on 2024-01-18 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_auto_20240110_2311"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartorder",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("shipped", "Shipped"),
                    ("delivered", "Delivered"),
                    ("process", "Processing"),
                ],
                default="Processing",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("disabled", "Disabled"),
                    ("in_review", "In Review"),
                    ("published", "Published"),
                    ("draft", "Draft"),
                    ("rejected", "Rejected"),
                ],
                default="in_review",
                max_length=10,
            ),
        ),
    ]
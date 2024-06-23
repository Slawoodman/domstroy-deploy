# Generated by Django 3.2.18 on 2024-01-09 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_auto_20240107_2015"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartorder",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("shipped", "Shipped"),
                    ("process", "Processing"),
                    ("delivered", "Delivered"),
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
                    ("disabled", "Disabled"),
                    ("draft", "Draft"),
                    ("in_review", "In Review"),
                    ("published", "Published"),
                    ("rejected", "Rejected"),
                ],
                default="in_review",
                max_length=10,
            ),
        ),
    ]

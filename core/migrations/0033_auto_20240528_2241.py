# Generated by Django 3.2.18 on 2024-05-28 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0032_auto_20240528_1914"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("shipped", "Shipped"),
                    ("process", "Processing"),
                    ("delivered", "Delivered"),
                ],
                default="Processing",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("published", "Published"),
                    ("in_review", "In Review"),
                    ("draft", "Draft"),
                    ("rejected", "Rejected"),
                    ("disabled", "Disabled"),
                ],
                default="in_review",
                max_length=10,
            ),
        ),
    ]
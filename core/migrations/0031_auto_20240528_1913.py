# Generated by Django 3.2.18 on 2024-05-28 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0030_auto_20240528_1911"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("delivered", "Delivered"),
                    ("process", "Processing"),
                    ("shipped", "Shipped"),
                ],
                default="Processing",
                max_length=10,
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
            model_name="vendor",
            name="description",
            field=models.TextField(
                blank=True, default="I am am Amazing Vendor", null=True
            ),
        ),
    ]

# Generated by Django 3.2.18 on 2023-12-29 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_auto_20231229_0438"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="digital",
        ),
        migrations.AddField(
            model_name="product",
            name="product_character",
            field=models.CharField(
                choices=[("new", "NEW"), ("used", "USED")], default="new", max_length=10
            ),
        ),
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
                    ("draft", "Draft"),
                    ("disabled", "Disabled"),
                    ("published", "Published"),
                    ("rejected", "Rejected"),
                    ("in_review", "In Review"),
                ],
                default="in_review",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="productreview",
            name="rating",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (1, "★☆☆☆☆"),
                    (2, "★★☆☆☆"),
                    (3, "★★★☆☆"),
                    (4, "★★★★☆"),
                    (5, "★★★★★"),
                ],
                null=True,
            ),
        ),
    ]
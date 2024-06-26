# Generated by Django 3.2.18 on 2023-12-29 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_auto_20231229_0435"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="product_status",
            field=models.CharField(
                choices=[
                    ("in_review", "In Review"),
                    ("draft", "Draft"),
                    ("rejected", "Rejected"),
                    ("disabled", "Disabled"),
                    ("published", "Published"),
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
                    ("1", "★✩✩✩✩"),
                    ("2", "★★✩✩✩"),
                    ("4", "★★★★✩"),
                    ("5", "★★★★★"),
                    ("3", "★★★✩✩"),
                ],
                null=True,
            ),
        ),
    ]

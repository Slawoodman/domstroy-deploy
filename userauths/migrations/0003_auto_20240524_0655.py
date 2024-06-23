# Generated by Django 3.2.18 on 2024-05-24 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userauths", "0002_profile_address"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="full_name",
        ),
        migrations.RemoveField(
            model_name="user",
            name="second_name",
        ),
        migrations.AddField(
            model_name="user",
            name="full_name",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
    ]

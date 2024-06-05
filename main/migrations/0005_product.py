# Generated by Django 5.0.1 on 2024-06-05 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_remove_profile_email_remove_profile_first_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("title", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to="product_images/")),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("category", models.CharField(max_length=50)),
                ("description", models.TextField()),
            ],
        ),
    ]
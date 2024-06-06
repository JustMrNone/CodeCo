# Generated by Django 5.0.1 on 2024-06-06 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0008_cart_cartitem"),
    ]

    operations = [
        migrations.CreateModel(
            name="EduPost",
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
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("image", models.ImageField(upload_to="edu_posts/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

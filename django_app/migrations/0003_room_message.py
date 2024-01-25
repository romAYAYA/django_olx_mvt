# Generated by Django 5.0.1 on 2024-01-25 13:40

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("django_app", "0002_itemrating"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Room",
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
                (
                    "name",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        default="",
                        max_length=300,
                        verbose_name="Name",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        default="",
                        max_length=300,
                        unique=True,
                        verbose_name="URL",
                    ),
                ),
            ],
            options={
                "ordering": ("-slug", "-name"),
            },
        ),
        migrations.CreateModel(
            name="Message",
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
                (
                    "content",
                    models.TextField(
                        blank=True, default="", verbose_name="Message text"
                    ),
                ),
                (
                    "date_added",
                    models.DateTimeField(
                        blank=True,
                        db_index=True,
                        default=django.utils.timezone.now,
                        max_length=300,
                        verbose_name="Date and time of creation",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        default="",
                        max_length=100,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        blank=True,
                        default="",
                        max_length=100,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="django_app.room",
                        verbose_name="Room",
                    ),
                ),
            ],
            options={
                "ordering": ("-date_added", "-room"),
            },
        ),
    ]

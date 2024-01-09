from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class CategoryItem(models.Model):
    title = models.CharField(
        verbose_name="Name",
        db_index=True,
        primary_key=False,
        unique=True,
        editable=True,
        blank=True,
        null=False,
        default="",
        max_length=300,
    )
    slug = models.SlugField(
        verbose_name="URL",
        db_index=True,
        primary_key=False,
        unique=True,
        editable=True,
        blank=True,
        null=False,
        default="",
        max_length=300,
    )

    class Meta:
        app_label = "django_app"
        ordering = ("-title",)
        verbose_name = ("Category",)
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"<CategoryItem {self.title}({self.id}) = {self.slug} />"


class TagItem(models.Model):
    title = models.CharField(
        verbose_name="Name",
        db_index=True,
        primary_key=False,
        unique=True,
        editable=True,
        blank=True,
        null=False,
        default="",
        max_length=300,
    )
    slug = models.SlugField(
        verbose_name="URL",
        db_index=True,
        primary_key=False,
        unique=True,
        editable=True,
        blank=True,
        null=False,
        default="",
        max_length=300,
    )

    class Meta:
        app_label = "django_app"
        ordering = ("-title",)
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return f"<TagItem {self.title} ({self.id}) = {self.slug} />"


class Item(models.Model):
    title = models.CharField(
        verbose_name="Name",
        db_index=True,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        default="",
        max_length=300,
    )
    description = models.TextField(
        verbose_name="Description",
        db_index=False,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        default="",
    )
    price = models.PositiveIntegerField(
        verbose_name="Price",
        db_index=False,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        default="",
    )
    category = models.ForeignKey(
        verbose_name="Category",
        db_index=True,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        default="",
        max_length=100,
        #
        to=CategoryItem,
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(
        verbose_name="Tags",
        db_index=True,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        default="",
        max_length=100,
        #
        to=TagItem,
    )
    is_active = models.BooleanField(
        verbose_name="Item activity", null=False, default=True
    )

    class Meta:
        app_label = "django_app"
        ordering = (
            "is_active",
            "-title",
        )
        verbose_name = ("Item",)
        verbose_name_plural = "Items"

    def __str__(self):
        if self.is_active:
            active = ("active",)
        else:
            active = ("sold",)
        return f"<Item {self.title}({self.id}) | {active} | {self.description[:30]} />"


class Vip(models.Model):
    article = models.OneToOneField(
        verbose_name="Article",
        db_index=True,
        primary_key=False,
        editable=True,
        blank=True,
        null=False,
        default="",
        max_length=100,
        #
        to=Item,
        on_delete=models.CASCADE,
    )
    priority = models.IntegerField(
        verbose_name="Priority",
        db_index=True,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        default=5,
    )
    expired = models.DateTimeField(
        verbose_name="Date and time of expiration",
        db_index=True,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        default=timezone.now,
        max_length=300,
    )

    class Meta:
        app_label = "django_app"
        ordering = (
            "priority",
            "-expired",
        )
        verbose_name = "Vip item"
        verbose_name_plural = "Vip items"

    def __str__(self):
        return f"<Vip {self.article.title}({self.id}) | {self.priority} / >"


class CommentItem(models.Model):
    author = models.ForeignKey(
        verbose_name="Author",
        db_index=True,
        primary_key=False,
        editable=True,
        blank=True,
        null=False,
        default="",
        max_length=100,
        #
        to=User,
        on_delete=models.CASCADE,
    )
    article = models.ForeignKey(
        verbose_name="Article",
        db_index=True,
        primary_key=False,
        editable=True,
        unique=False,
        blank=True,
        null=False,
        default="",
        max_length=100,
        #
        to=Item,
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name="Comment text",
        db_index=False,
        primary_key=False,
        editable=True,
        unique=False,
        blank=True,
        null=False,
        default="",
    )
    created = models.DateTimeField(
        verbose_name="Date and time of creation",
        db_index=True,
        primary_key=False,
        unique=False,
        editable=True,
        blank=True,
        null=False,
        default=timezone.now,
        max_length=300,
    )
    is_active = models.BooleanField(
        verbose_name="Activity",
        null=False,
        default=True,
    )

    class Meta:
        app_label = "django_app"
        ordering = ("-created",)
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"<CommentItem {self.article.title} ({self.id}) />"

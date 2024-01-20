import datetime
import re

from django.shortcuts import render, redirect
from django_app import models
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def home(request):
    categories = models.CategoryItem.objects.all()
    vips = (
        models.Vip.objects.all()
        .filter(expired__gt=datetime.datetime.now())
        .order_by("priority", "-article")
    )

    return render(request, "HomePage.html", {"categories": categories, "vips": vips})


def search(request):
    if request.method == "POST":
        _search = request.POST.get("search", "")
        _items = models.Item.objects.all().filter(
            is_active=True, title__icontains=_search
        )
        return render(request, "ItemsList.html", {"items": _items})


def items_list(request):
    _items = (
        models.Item.objects.all().filter(is_active=True).order_by("-price", "-title")
    )

    return render(request, "ItemsList.html", {"items": _items})


def category(request):
    categories = models.CategoryItem.objects.all()
    return render(request, "CategoryPage.html", {"categories": categories})


def items(request, slug: str):
    _category = models.CategoryItem.objects.get(slug=slug)
    _items = models.Item.objects.all().filter(is_active=True, category=_category)
    return render(request, "ItemsList.html", {"items": _items})


def item(request, item_id: str):
    _item = models.Item.objects.get(id=int(item_id))
    _comments = (
        models.CommentItem.objects.all()
        .filter(article=_item, is_active=True)
        .order_by("-created")
    )
    _ratings = models.ItemRating.objects.all().filter(item=_item)
    total_rating = (
        _ratings.filter(is_like=True).count() - _ratings.filter(is_like=False).count()
    )
    _is_user_rating = 1
    _is_user_rating = 0
    _is_user_rating = -1
    user_rating = _ratings.filter(author=request.user)
    if len(user_rating) > 0:
        _is_user_rating = 1 if user_rating[0].is_like else -1
    else:
        _is_user_rating = 0

    selected_page = request.GET.get(key="page", default=1)
    page_objs = Paginator(object_list=_comments, per_page=4)
    page_obj = page_objs.page(number=selected_page)

    return render(
        request,
        "ItemDetail.html",
        context={
            "item": _item,
            "page_obj": page_obj,
            "total_rating": total_rating,
            "is_user_rating": _is_user_rating,
        },
    )


def comment(request):
    if request.method == "POST":
        text = request.POST.get("text", "")
        article_id = request.POST.get("article", "")
        _item = models.Item.objects.get(id=int(article_id))
        models.CommentItem.objects.create(author=request.user, article=_item, text=text)
        return redirect(reverse("item", args=(article_id,)))


def register(request):
    if request.method == "GET":
        return render(request, "RegisterPage.html")
    elif request.method == "POST":
        username = str(request.POST["username"])
        password = str(request.POST["password"])
        # if not re.match(
        #     r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$',
        #     password,
        # ):
        #     return render(
        #         request,
        #         "RegisterPage.html",
        #         {"error": "Password does not match the complexity"},
        #     )
        user = User.objects.create(username=username, password=make_password(password))
        login(request, user)
        return redirect(reverse("home"))


def login_v(request):
    if request.method == "GET":
        return render(request, "LoginPage.html")
    elif request.method == "POST":
        username = str(request.POST["username"])
        password = str(request.POST["password"])

        user = authenticate(username=username, password=password)
        if user is None:
            return render(
                request, "LoginPage.html", {"error": "Login or Password don't match"}
            )
        login(request, user)
        return redirect(reverse("home"))


def logout_v(request):
    logout(request)
    return redirect(reverse("login"))


def rating(request, item_id: str, is_like: str):
    author = request.user
    _item = models.Item.objects.get(id=int(item_id))
    _is_like = True if is_like == "1" else False

    try:
        like_obj = models.ItemRating.objects.get(author=author, item=_item)
        if like_obj.is_like and _is_like:
            like_obj.delete()
        elif not like_obj.is_like and not _is_like:
            like_obj.delete()
        else:
            like_obj.is_like = _is_like
            like_obj.save()
    except Exception as _:
        like_obj = models.ItemRating.objects.create(
            author=author, item=_item, is_like=_is_like
        )

    return redirect(reverse("item", args=(item_id,)))

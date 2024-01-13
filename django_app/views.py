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
    _comments = models.CommentItem.objects.all().filter(is_active=True)

    selected_page = request.GET.get(key="page", default=1)
    page_objs = Paginator(object_list=_comments, per_page=4)
    page_obj = page_objs.page(number=selected_page)

    return render(
        request, "ItemDetail.html", context={"item": _item, "page_obj": page_obj}
    )


def comment(request):
    if request.method == "POST":
        text = request.POST.get("text", "")
        article_id = request.POST.get("article", "")
        _item = models.Item.objects.get(id=int(article_id))
        models.CommentItem.objects.create(author=request.user, article=_item, text=text)
        return redirect(reverse(("item"), args=(article_id,)))


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

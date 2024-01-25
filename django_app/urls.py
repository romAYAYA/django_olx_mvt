from django.urls import path
from django_app import views


urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("category/", views.category, name="category"),
    path("category/<str:slug>/", views.items, name="items"),
    path("item/<str:item_id>/", views.item, name="item"),
    path("comment/", views.comment, name="comment"),
    path("register/", views.register, name="register"),
    path("login/", views.login_v, name="login"),
    path("logout/", views.logout_v, name="logout"),
    path("item/<str:item_id>/rating/<str:is_like>", views.rating, name="rating"),
    path("chat/", views.chat, name="chat"),
    path("chat/<slug:room_slug>/", views.room, name="room"),
]

from django_app import views_a

websocket_urlpatterns = [
    path("ws/chat/<slug:room_name>/", views_a.ChatConsumer.as_asgi())
]

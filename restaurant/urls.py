from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("menu/", views.menu, name="menu"),
    path("menu/item/<int:pk>/", views.menu_item, name="menu_item"),
    path("book/", views.booking, name="book"),
]

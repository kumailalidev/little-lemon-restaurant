from django.shortcuts import render
from .models import Menu


def home(request):
    return render(request, "restaurant/index.html")


def about(request):
    return render(request, "restaurant/about.html")


def menu(request):
    menu_data = Menu.objects.all()
    context = {
        "menu": menu_data,
    }

    return render(request, "restaurant/menu.html", context)

from django.shortcuts import get_object_or_404, render
from .models import Menu
from .forms import BookingForm


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


def menu_item(request, pk=None):
    menu_item = get_object_or_404(Menu, pk=pk)

    return render(request, "restaurant/menu_item.html", {"menu_item": menu_item})


def book(request):
    form = BookingForm()

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {
        "form": form,
    }

    return render(request, "restaurant/book.html", context)

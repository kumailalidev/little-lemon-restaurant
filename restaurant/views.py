from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core import serializers

from .models import Menu, Booking
from .forms import BookingForm

from datetime import datetime
import json


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


@csrf_exempt
def bookings(request):
    """
    Bookings view for adding bookings to database and returning the JSON
    object containing current bookings present in database based on provided
    date.
    """

    if request.method == "POST":
        # get the JSON format data
        data = json.load(request)

        # returns True if QuerySet exists else returns False
        exist = (
            Booking.objects.filter(reservation_date=data["reservation_date"])
            .filter(reservation_slot=data["reservation_slot"])
            .exists()
        )
        # create a booking if there is empty slot else return error.
        if exist == False:
            # create an booking object in database
            booking = Booking(
                first_name=data["first_name"],
                reservation_date=data["reservation_date"],
                reservation_slot=data["reservation_slot"],
            )
            booking.save()
        else:
            return HttpResponse("{'error': 1}", content_type="application/json")

    # get date request parameter, if it doesn't exists assign python datetime value
    date = request.GET.get("date", datetime.today().date())

    # get booking QuerySet, filtered based on current date
    bookings = Booking.objects.all().filter(reservation_date=date)

    # convert bookings QuerySet object into JSON format
    booking_json = serializers.serialize("json", bookings)

    # return HTTP response contains JSON object.
    return HttpResponse(booking_json, content_type="application/json")


def reservations(request):
    # TODO: filter reservations based on current date
    bookings = Booking.objects.all()
    bookings_json = serializers.serialize("json", bookings)
    context = {
        "bookings": bookings,
    }

    return render(request, "restaurant/bookings.html", context)

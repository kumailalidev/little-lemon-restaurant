from django.forms import ModelForm

from .models import Booking


class BookingForm(ModelForm):
    """
    Booking form for getting booking data from user.
    """

    class Meta:
        model = Booking
        fields = "__all__"

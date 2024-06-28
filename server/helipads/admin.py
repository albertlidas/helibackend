from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Departure
from .models import Helicopter
from .models import RegularUser
from .models import HelipadOwner
from .models import Route
from .models import Ticket
from .models import Seat

admin.site.unregister(Group)


class DepartureModelAdmin(admin.ModelAdmin):
    list_display = ('route', 'departure_time', 'arrival_time', 'helicopter',)

    class Meta:
        model = Departure


class TicketModelAdmin(admin.ModelAdmin):
    list_display = ('departure', 'user', 'first_name', 'last_name', 'seat_number',)

    class Meta:
        model = Ticket


class SeatModelAdmin(admin.ModelAdmin):
    list_display = ('number_of_seat', 'departure_route', 'departure_time', 'ticket',)

    class Meta:
        model = Seat


admin.site.register(Departure, DepartureModelAdmin)
admin.site.register(HelipadOwner)
admin.site.register(Route)
admin.site.register(Helicopter)
admin.site.register(RegularUser)
admin.site.register(Ticket, TicketModelAdmin)
admin.site.register(Seat, SeatModelAdmin)

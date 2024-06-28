from collections import OrderedDict
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework_bulk import BulkSerializerMixin
from .models import Ticket, Seat, Departure, Helicopter, HelipadOwner, Route, RegularUser

"""Serializers for Managers and Users

"""


class RouteHelicopterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('starting_point', 'destination_point',)


class RegularUserPSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RegularUser
        fields = ('firstname', 'lastname', 'phone',)


class HelipadOwnerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HelipadOwner
        fields = ('organization', 'country', 'city', 'address', 'phone', 'contact_name',)


class UserSerializer(serializers.ModelSerializer):
    profile = HelipadOwnerSerializer(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'profile',)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        HelipadOwner.objects.create(user=user, **profile_data)
        return user


class RegularUserSerializer(serializers.ModelSerializer):
    profile = RegularUserPSerializer(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'profile',)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        RegularUser.objects.create(user=user, **profile_data)
        return user


"""Serializers for Helicopters

"""


class HelicopterSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='get_full_image_path')

    class Meta:
        model = Helicopter
        fields = ('id', 'title', 'seats_count', 'image',)


"""Serializers for Routes

"""


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('id', 'starting_point', 'latitude_start', 'longitude_start',
                  'latitude_end', 'longitude_end', 'destination_point',)


class RouteWithFlightsSerializer(serializers.ModelSerializer):
    departures = serializers.SerializerMethodField()

    def get_departures(self, obj):
        departures = Route.objects.get(pk=obj.id).departure_set.all()
        serializer = DeparturePlacesSerializer(instance=departures, many=True)
        return serializer.data

    class Meta:
        model = Route
        fields = ('id', 'departures', 'starting_point', 'latitude_start', 'longitude_start',
                  'latitude_end', 'longitude_end', 'destination_point',)


"""Serializers for Departures

"""


class DepartureCreateSerializer(serializers.ModelSerializer):
    helicopter = HelicopterSerializer()
    departure_id = serializers.IntegerField(source='id')

    def get_helicopter(self, obj):
        helicopter = Helicopter.objects.get(pk=obj.helicopter_id)
        serializer = HelicopterSerializer(instance=helicopter, many=False)
        return serializer.data

    class Meta:
        model = Departure
        fields = (
            'departure_id', 'helicopter', 'ticket_cost', 'route', 'departure_time', 'arrival_time', 'pilot1', 'pilot2', 'board',)


class DepartureSerializer(serializers.ModelSerializer):
    helicopter_id = serializers.PrimaryKeyRelatedField(source='helicopter', queryset=Helicopter.objects.all())

    class Meta:
        model = Departure
        fields = (
            'id', 'helicopter_id', 'ticket_cost', 'route', 'departure_time', 'arrival_time', 'pilot1', 'pilot2',
            'board',)


class DeparturePlacesSerializer(serializers.ModelSerializer):
    seats = serializers.SerializerMethodField('get_booked_seats')
    helicopter = HelicopterSerializer(many=False, read_only=True)
    departure_id = serializers.IntegerField(source='id')

    def get_booked_seats(self, obj):
        seats = Departure.objects.get(pk=obj.id).seat_set.all()
        serializer = SeatingSerializer(instance=seats, many=True)
        return serializer.data

    class Meta:
        model = Departure
        fields = (
            'departure_id', 'helicopter', 'ticket_cost', 'route', 'departure_time', 'arrival_time', 'pilot1', 'pilot2',
            'board', 'seats',)


class DepartureAroundSerializer(serializers.ModelSerializer):
    available_places = serializers.SerializerMethodField()
    helicopter = HelicopterSerializer(many=False, read_only=True)
    departure_title = serializers.CharField(source='route.starting_point')
    arrival_title = serializers.CharField(source='route.destination_point')
    departure_id = serializers.IntegerField(source='id')

    def get_available_places(self, obj):
        seats = Departure.objects.get(pk=obj.id).seat_set.filter(ticket__isnull=True)
        serializer = AvailableSeatsSerializer(instance=seats, many=True)
        return serializer.data

    class Meta:
        model = Departure
        fields = (
            'departure_id', 'helicopter', 'ticket_cost', 'route', 'departure_time', 'arrival_time', 'pilot1', 'pilot2',
            'board',
            'departure_title', 'arrival_title', 'available_places',)


"""Serializers for Seats

"""


class AvailableSeatsSerializer(serializers.ModelSerializer):
    seat_id = serializers.IntegerField(source='id')

    class Meta:
        model = Seat
        fields = ('seat_id', 'number_of_seat')


class SeatSerializer(serializers.ModelSerializer):
    free_seats = serializers.ListField(source='get_free_places')

    class Meta:
        model = Departure
        fields = ('free_seats',)

"""TicketSerializer for SeatingSerializer below

"""
class TicketPassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('first_name', 'last_name', 'phone', 'email',)


class SeatingSerializer(serializers.ModelSerializer):
    passenger = TicketPassengerSerializer(many=False, read_only=True, source='ticket')
    seat = serializers.CharField(source='number_of_seat')

    class Meta:
        model = Seat
        fields = ('seat', 'passenger',)

    def to_representation(self, instance):
        ret = OrderedDict()
        fields = [field for field in self.fields.values() if not field.write_only]

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            if attribute is not None:
                representation = field.to_representation(attribute)
                if representation is None:
                    continue
                if isinstance(representation, list) and not representation:
                    continue
                ret[field.field_name] = representation
        return ret


"""Serializers for Tickets

"""


class TicketHistorySerializer(serializers.ModelSerializer):
    route = serializers.CharField(source='__str__')
    departure_time = serializers.CharField(source='departure.departure_time')
    arrival_time = serializers.CharField(source='departure.arrival_time')

    class Meta:
        model = Ticket
        fields = (
            'first_name', 'last_name', 'phone', 'email', 'seat_number', 'route', 'departure_time', 'arrival_time',)


"""BOOKING

"""


class BookingSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    seat_id = serializers.PrimaryKeyRelatedField(source='place', queryset=Seat.objects.all())

    class Meta(object):
        model = Ticket
        # list_serializer_class = BulkListSerializer
        fields = ('departure', 'seat_id', 'first_name', 'last_name', 'phone', 'email',)

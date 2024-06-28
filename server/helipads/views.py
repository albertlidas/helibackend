from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
import datetime
from django.utils import timezone
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from django.core.mail import send_mail
from rest_framework.authentication import TokenAuthentication
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_bulk import ListBulkCreateAPIView
from django.contrib.auth.models import User
from django.conf import settings
from .models import *
from .serializers import *


# API for Users Login
# Return token and information about user.


class ObtainOwnerAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        country = user.helipadowner.country
        organization = user.helipadowner.organization
        city = user.helipadowner.city
        address = user.helipadowner.address
        email = user.email
        phone = user.helipadowner.phone
        contact_name = user.helipadowner.contact_name
        return Response(
            {'token': token.key, "organization": organization, "country": country, "city": city, "address": address,
             "email": email, "phone": phone, "contact_name": contact_name})


class ObtainUserAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        username = user.username
        lastname = user.regularuser.lastname
        firstname = user.regularuser.firstname
        email = user.email
        phone = user.regularuser.phone
        return Response({'token': token.key, "username": username, "firstname": firstname, "lastname": lastname,
                         "email": email, "phone": phone,})


# API for Users Logout


class UserLogout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class RestorePassword(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get(self, request, format=None):
        try:
            message = 'Password: {}'.format(self.request.user.password)
            print(self.request.user.password)
            print(self.request.user.email)
            send_mail('Password Restore', message, self.request.user.email,
                      [self.request.user.email, ], fail_silently=False)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# User Creation APIs


class CreateUpdateUser(CreateAPIView, UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CreateUpdateOwner(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = HelipadOwner.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            CreateAPIView.create(self, request, *args, **kwargs)
            return Response(status=None)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateUpdateRegularUser(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegularUserSerializer
    queryset = RegularUser.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            CreateAPIView.create(self, request, *args, **kwargs)
            return Response(status=None)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# APIs accessible by anyone


class ShowDeparturesAround(APIView):
    def post(self, request):
        user_latitude = request.data['from']['latitude']
        user_longitude = request.data['from']['longitude']
        user_location = GEOSGeometry('POINT({0} {1})'.format(user_longitude, user_latitude))
        limit = request.data['limit']
        query_start, query_end = limit.split(',')

        routes_query = Route.objects.filter(starting_location__distance_lte=(user_location, D(km=100)))
        departures_query = Departure.objects.filter(id__in=routes_query.values('departure')).order_by('departure_time')

        if request.data.get('time'):
            time_format = '%Y-%m-%d'
            date_object = datetime.datetime.strptime(request.data.get('time'), time_format)
            departures_query = departures_query.filter(departure_time__gt=date_object)

        if request.data.get('to'):
            destination_latitude = request.data['to']['latitude']
            destination_longitude = request.data['to']['longitude']
            destination_location = GEOSGeometry('POINT({0} {1})'.format(destination_longitude, destination_latitude))

            departures_query = departures_query.filter(
                route__destination_location__distance_lte=(destination_location, D(km=100)))

        departures_query = departures_query[int(query_start): int(query_end)]
        serializer = DepartureAroundSerializer(departures_query, many=True)
        return Response(serializer.data)


# APIs accessible by regular users
# Those are the users that order tickets and fly.


class ShowFlightHistory(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TicketHistorySerializer

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)


class BookSeats(ListBulkCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = BookingSerializer
    queryset = Ticket.objects.all()

    def perform_create(self, serializer):
        for data_entry in self.request.data:
            seat = Seat.objects.get(pk=data_entry['seat_id'])
            if seat.ticket is not None:
                raise serializers.ValidationError("Seat " + str(seat.number_of_seat) + " is already occupied")

            if seat.departure.departure_time < timezone.now():
                raise serializers.ValidationError("Flight already happened")

        serializer.save(user_id=self.request.user.id)

        for data_entry in self.request.data:
            seat = Seat.objects.get(pk=data_entry['seat_id'])
            ticket = Ticket.objects.get(place=seat.id)
            ticket.seat_number = seat.number_of_seat
            ticket.save()
            seat.ticket = ticket
            seat.save()
            try:
                message = 'Name: {} \n\nLast Name: {} \n\nSeat Number: {} \n\nRoute: {} \n\nDeparture Time: {}'.format(
                    data_entry['first_name'], data_entry['last_name'], str(ticket.seat_number), ticket.__str__(),
                    str(ticket.departure.departure_time))
                send_mail('Ticket', message, data_entry['email'],
                          [data_entry['email'], ], fail_silently=False)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)


class ShowDeparture(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DepartureAroundSerializer
    queryset = Departure.objects.all()


# Helipad Manager's APIs



class ShowRoutes(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RouteSerializer

    def get_queryset(self):
        id = self.request.user.id
        return User.objects.get(pk=id).route_set.all()


class CreateDeleteRoute(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RouteSerializer
    queryset = Route.objects.all()

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class ShowRoutesWithFlights(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RouteWithFlightsSerializer

    def get_queryset(self):
        id = self.request.user.id
        return User.objects.get(pk=id).route_set.all()


class ShowHelicopters(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = HelicopterSerializer
    queryset = Helicopter.objects.all()


class ShowDepartures(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DeparturePlacesSerializer

    def get_queryset(self):
        id = self.kwargs['route_id']
        return Route.objects.get(pk=id).departure_set.all()


class CreateDeparture(APIView):
    def post(self, request, format=None):
        serializer = DepartureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            helicopter_object = Helicopter.objects.get(pk=serializer.data['helicopter_id'])
            helicopter = {'id': helicopter_object.id, 'title': helicopter_object.title,
                          'seats_count': helicopter_object.seats_count,
                          'image': helicopter_object.get_full_image_path()}
            response_serializer_data = {'departure_id': serializer.data['id'],
                                        'departure_time': serializer.data['departure_time'],
                                        'arrival_time': serializer.data['arrival_time'],
                                        'route': serializer.data['route'],
                                        'pilot1': serializer.data['pilot1'], 'pilot2': serializer.data['pilot2'],
                                        'board': serializer.data['board'],
                                        'ticket_cost': serializer.data['ticket_cost'],
                                        'helicopter': helicopter}

            response_serializer = DepartureCreateSerializer(data=response_serializer_data)
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteDeparture(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DepartureSerializer
    queryset = Departure.objects.all()

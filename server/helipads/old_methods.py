
""" VIEWS

"""

class AllDepartures(APIView):
    def post(self, request):
        user_latitude = request.data['from']['latitude']
        user_longitude = request.data['from']['longitude']
        user_location = GEOSGeometry('POINT({0} {1})'.format(user_longitude, user_latitude))
        limit = request.data['limit']
        query_start, query_end = limit.split(',')

        helipad_query = Helipad.objects.filter(location__distance_lte=(user_location, D(km=100)))
        departures_query = Departure.objects.filter(id__in=helipad_query.values('departure')).order_by('departure_time')

        if request.data.get('time'):
            import datetime
            # from django.utils.timezone import get_current_timezone
            # tz = get_current_timezone()

            time_format = '%Y-%m-%d'
            date_object = datetime.datetime.strptime(request.data.get('time'), time_format)
            departures_query = departures_query.filter(departure_time__gt=date_object)

        if request.data.get('to'):
            destination_latitude = request.data['to']['latitude']
            destination_longitude = request.data['to']['longitude']
            destination_location = GEOSGeometry('POINT({0} {1})'.format(destination_longitude, destination_latitude))

            departures_query = departures_query.filter(destination__to__distance_lte=(destination_location, D(km=100)))

        departures_query = departures_query[int(query_start): int(query_end)]
        serializer = DepartureSerializer(departures_query, many=True)
        return Response(serializer.data)



class BookSeat(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, id):
        departure = get_object_or_404(Departure, pk=id)
        if request.data['seats']:
            seats = request.data['seats']
            for seat_number in seats:
                if not getattr(departure, 'place{}'.format(seat_number['id'])):
                    setattr(departure, 'place{}'.format(seat_number['id']), True)
                else:
                    serializer = SeatSerializer(departure, many=False)
                    return Response(serializer.data, status=status.HTTP_410_GONE)
            departure.save()
            try:
                print(request.user.email)
                message = 'You booked a seat!'
                send_mail('Booking', message, settings.EMAIL_HOST_USER,
                          [request.user.email], fail_silently=False)
                return Response(status=status.HTTP_201_CREATED)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)


class ClosestHelipadsList(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = HelipadSerializer
    user_location = None

    def get_serializer_context(self):
        return {'user_location': self.user_location}

    def get_queryset(self):
        longitude = self.request.query_params.get('longitude', None)
        latitude = self.request.query_params.get('latitude', None)
        self.user_location = GEOSGeometry('POINT({0} {1})'.format(longitude, latitude))
        closest_helipads = Helipad.objects.distance(self.user_location).order_by('distance')
        return closest_helipads



class DestinationList(mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):
    serializer_class = DestinationSerializer

    def get_queryset(self):
        helipad_id = self.kwargs['helipad_id']
        return Helipad.objects.get(pk=helipad_id).destination_set.all()



""" SERIALIZERS

"""

class DepartureSerializer(serializers.ModelSerializer):
    helipad_id = serializers.PrimaryKeyRelatedField(source='helipad', queryset=Helipad.objects.all())
    helipad_title = serializers.PrimaryKeyRelatedField(source='helipad.title', queryset=Helipad.objects.all())
    departure_location = serializers.PrimaryKeyRelatedField(source='helipad.departure_location',
                                                            queryset=Helipad.objects.all())
    destination_title = serializers.PrimaryKeyRelatedField(source='destination.title',
                                                           queryset=Destination.objects.all())
    places = serializers.ListField(source='get_free_places')

    class Meta:
        model = Departure
        fields = ('id', 'helipad_id', 'departure_location', 'departure_time', 'arrival_time', 'helipad_title', 'destination_title', 'places',)


class HelipadSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        return {
            'id': obj.id,
            'title': obj.title,
            'distance': obj.distance_to(self.context['user_location'])
        }


class DestinationSerializer(serializers.ModelSerializer):
    helipad_id = serializers.PrimaryKeyRelatedField(source='helipad', queryset=Helipad.objects.all())

    class Meta:
        model = Destination
        fields = ('id', 'helipad_id', 'to', 'info',)
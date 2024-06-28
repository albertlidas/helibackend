from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class HelipadOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    contact_name = models.CharField(max_length=50)
    organization = models.CharField(max_length=70)

    def __str__(self):
        return self.user.username


class RegularUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return str(self.user.firstname) + str(self.user.lastname)


class Helipad(models.Model):
    latitude = models.FloatField(max_length=20)
    longitude = models.FloatField(max_length=20)
    title = models.CharField(max_length=50)
    departure_location = models.CharField(max_length=50)
    objects = models.GeoManager()
    location = models.PointField(blank=True)

    def save(self, *args, **kwargs):
        self.location = Point(self.longitude, self.latitude)
        super(Helipad, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def distance_to(self, point):
        return self.location.distance(point) * 100000

    class Meta:
        verbose_name = 'helipad'
        verbose_name_plural = 'helipads'


class Destination(models.Model):
    title = models.CharField(max_length=20)
    helipad = models.ForeignKey(Helipad)
    latitude = models.FloatField(max_length=20)
    longitude = models.FloatField(max_length=20)
    objects = models.GeoManager()
    info = models.TextField(null=True)
    to = models.PointField(blank=True)

    def save(self, *args, **kwargs):
        self.to = Point(self.longitude, self.latitude)
        super(Destination, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'destination'
        verbose_name_plural = 'destinations'


class Route(models.Model):
    user = models.ForeignKey(User)
    latitude_start = models.FloatField(max_length=20)
    longitude_start = models.FloatField(max_length=20)
    latitude_end = models.FloatField(max_length=20)
    longitude_end = models.FloatField(max_length=20)
    starting_point = models.CharField(max_length=50)
    destination_point = models.CharField(max_length=50)
    objects = models.GeoManager()
    starting_location = models.PointField(blank=True)
    destination_location = models.PointField(blank=True)

    def save(self, *args, **kwargs):
        self.starting_location = Point(self.longitude_start, self.latitude_start)
        self.destination_location = Point(self.longitude_end, self.latitude_end)
        super(Route, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.starting_point) + ' - ' + str(self.destination_point)

    class Meta:
        verbose_name = 'route'
        verbose_name_plural = 'routes'


class Helicopter(models.Model):
    title = models.CharField(max_length=50)
    seats_count = models.IntegerField()
    image = models.ImageField(upload_to='helicopters')

    def __str__(self):
        return str(self.title)

    def get_full_image_path(self):
        return '/static/user_images/' + str(self.image)

    class Meta:
        verbose_name = 'helicopter'
        verbose_name_plural = 'helicopters'


class Departure(models.Model):
    helicopter = models.ForeignKey(Helicopter)
    route = models.ForeignKey(Route)
    departure_time = models.DateTimeField(max_length=50)
    arrival_time = models.DateTimeField(max_length=50)
    ticket_cost = models.IntegerField()
    pilot1 = models.CharField(max_length=50, null=True)
    pilot2 = models.CharField(max_length=50, null=True)
    board = models.IntegerField()
    place1 = models.BooleanField(default=False)
    place2 = models.BooleanField(default=False)
    place3 = models.BooleanField(default=False)
    place4 = models.BooleanField(default=False)

    def get_free_places(self):
        free_places = []
        for index in range(1, 5):
            if not getattr(self, 'place{}'.format(index)):
                free_places.append(index)
        return free_places

    def booked_seats(self):
        return Departure.objects.get(pk=self.id).seat_set.all()

    def __str__(self):
        return str(self.route.starting_point) + ' - ' + str(self.route.destination_point) + ' @ ' + str(
            self.departure_time)

    def save(self, *args, **kwargs):
        number_of_seats = int(self.helicopter.seats_count)
        super(Departure, self).save(*args, **kwargs)
        for i in range(1, number_of_seats + 1):
            seat = Seat(departure=self, number_of_seat=i)
            seat.save()

    class Meta:
        verbose_name = 'departure'
        verbose_name_plural = 'departures'




class Ticket(models.Model):
    departure = models.ForeignKey(Departure)
    user = models.ForeignKey(User)
    place = models.ForeignKey('Seat', related_name='+')
    seat_number = models.IntegerField(null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.departure.route.starting_point) + ' - ' + str(self.departure.route.destination_point)

    class Meta:
        verbose_name = 'ticket'
        verbose_name_plural = 'tickets'


class Seat(models.Model):
    departure = models.ForeignKey(Departure)
    ticket = models.ForeignKey(Ticket, blank=True, null=True)
    number_of_seat = models.IntegerField()

    def __str__(self):
        return str(self.number_of_seat)

    def departure_route(self):
        return str(self.departure.route.starting_point) + ' - ' + str(self.departure.route.destination_point)

    def departure_time(self):
        return str(self.departure.departure_time)

    class Meta:
        verbose_name = 'seat'
        verbose_name_plural = 'seats'

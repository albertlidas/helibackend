from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import *

urlpatterns = [
    url(r'^owner/login/$', ObtainOwnerAuthToken.as_view()),
    url(r'^owner/create/$', CreateUpdateOwner.as_view()),
    url(r'^owner/logout/', UserLogout.as_view()),
    url(r'^user/create/$', CreateUpdateRegularUser.as_view()),
    url(r'^user/login/$', ObtainUserAuthToken.as_view()),
    url(r'^user/password/restore/$', RestorePassword.as_view()),
    url(r'^user/logout/', UserLogout.as_view()),
    url(r'^departures/all/$', ShowDeparturesAround.as_view()),
    url(r'^departure/$', CreateDeparture.as_view()),
    url(r'^booking/', BookSeats.as_view()),
]

router = DefaultRouter()
router.register(r'route', CreateDeleteRoute, base_name='CreateDeleteRoute')
router.register(r'routes', ShowRoutes, base_name='Routes')
router.register(r'user/departure', ShowDeparture, base_name='Departure')
router.register(r'user/history', ShowFlightHistory, base_name='ShowFlightHistory')
router.register(r'departures/(?P<route_id>\d+)', ShowDepartures, base_name='Departures')
router.register(r'helicopters', ShowHelicopters, base_name='Helicopters')
router.register(r'departure', DeleteDeparture, base_name='DeleteDeparture')
router.register(r'routes_with_flights', ShowRoutesWithFlights, base_name='ShowRoutesWithFlights')

urlpatterns += router.urls


from hamcrest import *
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Helipad


class ClosestHelipadsTest(APITestCase):
    def setUp(self):
        helipad = Helipad(title='Odessa', latitude=3.7298583984376, longitude=8.8687133789063)
        self.request_string = '/api/v1/helipads/?latitude{}=&longitude={}'.format(helipad.latitude, helipad.longitude)

    def test_closest_helipads(self):
        response = self.client.get(self.request_string)
        correct_response = {'id': 1, 'title': 'Odessa', 'distance': 651.5020680357238}
        assert_that(response.content, equal_to(correct_response))

    def test_status_code(self):
        response = self.client.get(self.request_string)
        assert_that(response.status_code, equal_to(status.HTTP_200_OK))

    def test_incorrect_entry_data(self):
        latitude = 'x'
        longitude = 'z'
        request_string = '/api/v1/helipads/?latitude{}=&longitude={}'.format(latitude, longitude)
        response = self.client.get(request_string)
        assert_that(response.status_code, equal_to(status.HTTP_400_BAD_REQUEST))

    def test_bad_request_with_missing_coordinates(self):
        request_string = '/api/v1/helipads/'
        response = self.client.get(request_string)
        assert_that(response.status_code, equal_to(status.HTTP_400_BAD_REQUEST))

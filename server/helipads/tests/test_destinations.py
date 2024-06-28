from hamcrest import *
from rest_framework import status
from rest_framework.test import APITestCase

from helipads.models import Destination


class DestinationListTest(APITestCase):
    def setUp(self):
        self.id = 1
        self.api_path = '/api/v1/helipads/{}/destinations/'.format(self.id)

    def test_returns_correct_value(self):
        response = self.client.get(self.api_path)
        correct_response = {'name': 'Odessa'}
        assert_that(response.data, equal_to(correct_response))

    def test_status_code(self):
        response = self.client.get(self.api_path)
        assert_that(response.status_code, equal_to(status.HTTP_200_OK))

    def test_incorrect_entry_data(self):
        invalid_id = 'k'
        request_string = '/api/v1/helipads/{}/destinations'.format(invalid_id)
        response = self.client.get(request_string)
        assert_that(response.status_code, equal_to(status.HTTP_404_NOT_FOUND))

    def test_creates_destination(self):
        response = self.client.post(self.api_path, format='json')
        assert_that(response.status_code, equal_to(201))
        assert_that(Destination.objects.filter(helipad__id=1).count(), equal_to(1))

    def destination_data(self):
        return {
            # TODO add proper data
            '': ''
        }

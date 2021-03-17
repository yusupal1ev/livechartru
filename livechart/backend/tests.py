from django.test import TestCase
from django.http import HttpResponsePermanentRedirect, HttpResponseNotFound

from .views import *
from .models import Season


class TestHomeView(TestCase):
    def test_get_empty_season(self):
        response = self.client.get('')
        self.assertEqual(HttpResponseNotFound.status_code, response.status_code)

    def test_get(self):
        Season.objects.create(season='fall', year=2022, month_started=1, month_ended=3)
        response = self.client.get('')
        self.assertEqual(HttpResponsePermanentRedirect.status_code, response.status_code)

from django.test import TestCase, Client
from rest_framework import status
from django import urls
import json
from django.http import HttpRequest
from rest_framework import permissions, status
from rest_framework.response import Response
from ..models import *
import mock


class DiscountCodeViewSetTestCase(TestCase):

    def setUp(self):
        pass

    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()

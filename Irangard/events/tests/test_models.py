from django.test import TestCase
from ..models import Event
from accounts.models import User
from rest_framework.test import APIClient
from django.urls import reverse
import json
from rest_framework import status


class EventTestcase(TestCase):
    
    def setUp(self):
        return super().setUp()
    
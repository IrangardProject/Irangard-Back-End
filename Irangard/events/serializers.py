from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from .models import *
from accounts.models import User
from accounts.serializers.user_serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

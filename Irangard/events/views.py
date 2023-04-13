from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import DefaultPagination
from .models import Event
from .serializers import *
from .permissions import *
from .filters import EventFilter

from django.core.cache import cache


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsIsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination
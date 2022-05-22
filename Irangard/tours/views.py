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
from tours.models import *
from .serializers import *
from .permissions import *


class TourViewSet(ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    pagination_class = DefaultPagination
    permission_classes = [IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data
        title = data.pop('title', None)
        cost = data.pop('cost', None)
        capacity = data.pop('capacity', None)
        start_date = data.pop('start_date', None)
        end_date = data.pop('end_date', None)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tour = serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

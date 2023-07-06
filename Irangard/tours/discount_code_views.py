import json
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


from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.utils.decorators import method_decorator
from Irangard.settings import CACHE_TTL


class DicountCodeViewSet(ModelViewSet):

    serializer_class = DiscountCodeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    permission_classes = [IsDiscountCodeOwnerOrReadOnly]

    def get_queryset(self):
        return DiscountCode.objects.filter(
            tour_id=self.kwargs.get('tour_pk'))\
            .order_by('expire_date')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tour'] = self.kwargs.get('tour_pk')
        return context

    def create(self, request, *args, **kwargs):
        try:
            tour = get_object_or_404(Tour.objects, pk=self.kwargs.get('tour_pk'))
            if(len(DiscountCode.objects.filter(tour=tour).filter(code=request.data['code'])) > 0):
                return Response('the discount_code exists',status=status.HTTP_400_BAD_REQUEST) 
            data = request.data.copy()
            data['tour'] = tour.id
            serializer = DiscountCodeSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)


    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
      return super().list(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        
        discount_code = None
        tour_id = kwargs.get('tour_pk')
        discount_code_id = "DiscountCode"+str(kwargs.get('pk'))

        if(cache.get(discount_code_id)):
            discount_code = cache.get(discount_code_id)
            print('hit the cache')
        else:
            discount_code = self.get_object()
            cache.set(discount_code_id,discount_code)
            print("hit the db")

        serializer = self.get_serializer(discount_code)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
        discount_code = self.get_object()
        return self.perform_change(request, 'update', *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.perform_change(request, 'destroy', *args, **kwargs)

    def perform_change(self, request, action, *args, **kwargs):
        user = request.user
        discount_code = self.get_object()
        if not discount_code.is_owner(user):
            return Response('you do not have permission to change this discount-code.',
                            status=status.HTTP_403_FORBIDDEN)
        if action == 'update':
            serializer = self.get_serializer(
                discount_code, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            cache.set("DiscountCode"+str(discount_code.id),discount_code)
            print('update the cache')
            return Response(serializer.data, status=status.HTTP_200_OK)

        super().destroy(request, *args, **kwargs)
        cache.delete("DiscountCode"+str(discount_code.id))
        return Response('disount-code destroyed', status=status.HTTP_204_NO_CONTENT)

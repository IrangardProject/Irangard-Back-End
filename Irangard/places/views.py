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
from places.models import Place, PlaceStatus
from .serializers import *
from .permissions import *
from .filters import PlaceFilter

from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.utils.decorators import method_decorator
from Irangard.settings import CACHE_TTL
from utils.constants import ActionDimondExchange


class PlaceViewSet(ModelViewSet):
	queryset = Place.objects.all()
	serializer_class = PlaceSerializer
	filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
	# filterset_fields = ['place_type']
	filterset_class = PlaceFilter
	search_fields = ['title']  # space comma seprator
	ordering_fields = ['-rate']
	pagination_class = DefaultPagination
	permission_classes = [IsIsAuthenticatedOrReadOnly]

	def claim_place_ownership(self, user, place):
		record = PlaceStatus.objects.create(user=user, place=place)
		record.save()

	def create(self, request, *args, **kwargs):
		data = request.data.copy()
		images = data.pop('images', [])
		tags = data.pop('tags', [])
		features = data.pop('features', [])
		rooms = data.pop('rooms', [])
		optional_costs = data.pop('optional_costs', [])
		contact_data = data.pop('contact', None)
		hours_data = contact_data.pop(
			'working_hours', []) if contact_data else []

		serializer = self.get_serializer(data=data)
		serializer.is_valid(raise_exception=True)
		place = serializer.save()
		
		if contact_data:
			contact = Contact.objects.create(place=place, **contact_data)
		for hours in hours_data:
			Hours.objects.create(contact=contact, **hours)
		for image in images:
			Image.objects.create(place=place, image=image)
		for tag in tags:
			Tag.objects.create(place=place, **tag)
		for feature in features:
			Feature.objects.create(place=place, **feature)
		for room in rooms:
			Room.objects.create(place=place, **room)
		for optional_cost in optional_costs:
			Optional.objects.create(place=place, **optional_cost)

		# add claimed_place record if user claim place ownership
		claim_ownership = request.data.get('claim_ownership')
		if(claim_ownership):
			self.claim_place_ownership(request.user, place)
		# end add claimed_place
		headers = self.get_success_headers(serializer.data)
		user = request.user
		user.dimonds += ActionDimondExchange.ADDING_PLACE
		user.save()

		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


	# @method_decorator(cache_page(CACHE_TTL))
	# def list(self, request, *args, **kwargs):
	#     return super().list(self, request, *args, **kwargs)

	def retrieve(self, request, *args, **kwargs):
		place = None
		place_id = "Place"+str(self.kwargs.get("pk"))
		if(cache.get(place_id)):
			place = cache.get(place_id)
			print("hit the cache")
		else:
			place = self.get_object()
			cache.set(place_id, place)
			print("hit the db")
		serializer = self.get_serializer(place)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def update(self, request, *args, **kwargs):
		place = self.get_object()
		if not (place.is_adimn_or_owner(request.user) or place.is_added_by(request.user)):
			return Response('you do not have permission to edit this place.',
							status=status.HTTP_403_FORBIDDEN)
		data = request.data.copy()
		images = data.pop('images', None)
		tags = data.pop('tags', None)
		features = data.pop('features', None)
		rooms = data.pop('rooms', None)
		optional_costs = data.pop('optional_costs', None)
		contact_data = data.pop('contact', None)
		hours_data = contact_data.pop(
			'working_hours', None) if contact_data else None
		if contact_data:
			ContactSerializer().update(place.contact, contact_data)
		if hours_data:
			place.contact.working_hours.all().delete()
			for hours in hours_data:
				Hours.objects.create(contact=place.contact, **hours)
		if images:
			place.images.all().delete()
			for image in images:
				Image.objects.create(place=place, image=image)
		if tags:
			place.tags.all().delete()
			for tag in tags:
				Tag.objects.create(place=place, **tag)
		if features:
			place.features.all().delete()
			for feature in features:
				Feature.objects.create(place=place, **feature)
		if rooms:
			place.rooms.all().delete()
			for room in rooms:
				Room.objects.create(place=place, **room)
		if optional_costs:
			place.optional_costs.all().delete()
			for optional_cost in optional_costs:
				Optional.objects.create(place=place, **optional_cost)
		cache.set("Place"+str(place.id), place)
		print("update the cache")
		return super().update(request, *args, **kwargs)
		
	def destroy(self, request, *args, **kwargs):
		place = self.get_object()
		if not place.is_adimn_or_owner(request.user):
			return Response('you do not have permission to delete this place.',
							status=status.HTTP_403_FORBIDDEN)
		return super().destroy(request, *args, **kwargs)

	# def get_serializer_class(self):
	# 	place = self.get_object()
	# 	if place.place_type == 1:
	# 		return ResidenceSerializer
	# 	if place.place_type == 2:
	# 		return RecreationSerializer
	# 	if place.place_type == 3:
	# 		return AttractionSerializer
	#  	return super().get_serializer_class()

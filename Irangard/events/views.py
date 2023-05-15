from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import DefaultPagination
from .models import Event, Tag, Image
from .serializers import EventSerializer
from .permissions import EventPermission
from .filters import EventFilter
from django.utils import timezone
from utils.constants import StatusMode


class EventViewSet(ModelViewSet):
    queryset = Event.objects.filter(end_date__gte=timezone.now(), status=StatusMode.ACCEPTED)
    serializer_class = EventSerializer
    filterset_class = EventFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [EventPermission]
    pagination_class = DefaultPagination
    ordering_fields = ['date_created', 'start_date']
    
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        tags = data.pop('tags', [])
        images = data.pop('images', [])
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        
        for tag in tags:
            Tag.objects.create(event=event, **tag)
            
        for image in images:
            Image.objects.create(event=event, image=image)
            
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    def update(self, request, *args, **kwargs):
        event = self.get_object()
        data = request.data.copy()
        images = data.pop('images', None)
        tags = data.pop('tags', None)

        if images:
            event.images.all().delete()
            for image in images:
                Image.objects.create(event=event, image=image)

        if tags:
            event.tags.all().delete()
            for tag in tags:
                Tag.objects.create(event=event, **tag)

        return super().update(request, *args, **kwargs)

        
    def retrieve(self, request, *args, **kwargs):
        obj = get_object_or_404(Event, pk=kwargs['pk'])
        session_key = 'viewed_object_{}'.format(kwargs['pk'])
        if not request.session.get(session_key, False): 
            # to prevent a user's multiply view, count multiply times
            obj.views += 1
            obj.save()
            request.session[session_key] = True
        return super().retrieve(request, *args, **kwargs)
    
    
    @action(methods=['GET'], detail=False)
    def recommended_events(self, request):
        not_expired_events = [event for event in Event.objects.all() if not event.is_expired]
        sorted_events = sorted(not_expired_events, key=lambda t: t.recommendation_rate, reverse=True)
        serializer = self.get_serializer(sorted_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @action(detail=True, methods=['put'], permission_classes=[IsAdminUser])
    def admin_acceptance(self, request, pk=None):
        event = get_object_or_404(Event, pk=pk)
        if event.status == StatusMode.ACCEPTED:
            message = f"The event with ID {pk}, was already in accepted status."
            return Response(status=status.HTTP_200_OK, data={"message": message})
        
        event.status = StatusMode.ACCEPTED
        event.save()
        message = f"The event with ID {pk}, is now in accepted status."
        return Response(data={"message": message}, status=status.HTTP_200_OK)
    
    
    @action(detail=True, methods=['put'], permission_classes=[IsAdminUser])
    def admin_denial(self, request, pk=None):
        event = get_object_or_404(Event, pk=pk)
        if event.status == StatusMode.DENIED:
            message = f"The event with ID {pk}, was already in denied status."
            return Response(status=status.HTTP_200_OK, data={"message": message})
        
        event.status = StatusMode.ACCEPTED
        event.save()
        message = f"The event with ID {pk}, is now in denied status."
        return Response(data={"message": message}, status=status.HTTP_200_OK)

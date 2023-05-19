from rest_framework.viewsets import ModelViewSet
from .models import TourSuggestion, EventSuggestion, PlaceSuggestion
from .serializers import (TourSuggestionSerializer,
                        EventSuggestionSerializer, 
                        PlaceSuggestionSerializer)
from rest_framework.response import Response
from rest_framework import status
from .permissions import SuggestionPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


class SuggestionViewSet(ModelViewSet):
    permission_classes = [SuggestionPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['sender'] = self.request.user
        data = serializer.validated_data
        if data['sender'] == data['receiver']:
            return Response({'error': 'Sender and receiver cannot be the same.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if self.SuggestionModel.objects.filter(receiver=data['receiver'], sender=data['sender'], **self.suggestion_fields(data)):
            return Response(
                {'error': f'You have been suggested this {self.suggestion_name} to this user before'},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def sender_suggestions(self, request):
        user = request.user
        objs = self.SuggestionModel.objects.filter(sender=user)
        sorted_objs = sorted(objs, key=lambda obj: obj.date_created)
        serializer = self.serializer_class(sorted_objs, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def receiver_suggestions(self, request):
        user = request.user
        objs = self.SuggestionModel.objects.filter(receiver=user)
        sorted_objs = sorted(objs, key=lambda obj: obj.date_created)
        serializer = self.serializer_class(sorted_objs, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
        
    
class TourSuggestionViewSet(SuggestionViewSet):
    queryset = TourSuggestion.objects.all()
    serializer_class = TourSuggestionSerializer
    SuggestionModel = TourSuggestion
    suggestion_name = 'tour'
    suggestion_fields = lambda self, data: {'tour': data['tour']}


class EventSuggestionViewSet(SuggestionViewSet):
    queryset = EventSuggestion.objects.all()
    serializer_class = EventSuggestionSerializer
    SuggestionModel = EventSuggestion
    suggestion_name = 'event'
    suggestion_fields = lambda self, data: {'event': data['event']}


class PlaceSuggestionViewSet(SuggestionViewSet):
    queryset = PlaceSuggestion.objects.all()
    serializer_class = PlaceSuggestionSerializer
    SuggestionModel = PlaceSuggestion
    suggestion_name = 'place'
    suggestion_fields = lambda self, data: {'place': data['place']}

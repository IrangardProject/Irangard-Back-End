from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers.user_serializers import *
from .serializers.serializers import *
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .permissions import IsSpecialUser
from tours.serializers import TourSerializer

class SpecialUserViewSet(ModelViewSet):
    queryset = SpecialUser.objects.all()
    serializer_class = SpecialUserSerializer
    permission_classes = [IsSpecialUser]
    
    @action(detail=False, methods=['GET'], permission_classes=[IsSpecialUser])
    def tours(self, request):
        special_user = SpecialUser.objects.get(user=request.user)
        tours = TourSerializer(special_user.tours, many=True, context={"request": request})

        return Response(tours.data, status=status.HTTP_200_OK)
        
        

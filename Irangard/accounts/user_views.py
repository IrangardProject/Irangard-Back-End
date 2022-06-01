from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers.user_serializers import *
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

class UserProfile(GenericAPIView):
	queryset = User.objects.all()
	serializer_class = UserProfileSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
	
	def get(self, request, username, *args, **kwargs):
		parser_classes = [MultiPartParser, FormParser]
		
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			return Response({'error': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
		
		serializer = UserProfileSerializer(user, context = {'user': request.user})
		return Response(serializer.data)
	
	def put(self, request, username, *args, **kwargs):
		parser_classes = [MultiPartParser, FormParser]
		user = User.objects.get(username=username)
		# if(request.user != username):
		# 	return Response("token is not for given username", status=status.HTTP_400_BAD_REQUEST)
		# else:
		serializer = UserProfileSerializer(user, data=request.data, context = {'user': request.user})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
		



class FeediewSet(ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserFeedSerializer
	permission_classes = [IsAdminUser]
	
	@action(detail=True, permission_classes=[AllowAny],
			url_name="get-followers", url_path="followers")
	def get_followers(self, request, *args, **kwargs):
		user = self.get_object()
		serializer = UserFeedSerializer(
			user.followers, context={'user': request.user}, many=True)
		return Response(status=status.HTTP_200_OK, data=serializer.data)

	@action(detail=True, permission_classes=[AllowAny],
			url_name="get-following", url_path="following")
	def get_following(self, request, *args, **kwargs):
		user = self.get_object()
		serializer = UserFeedSerializer(
			user.following, context={'user': request.user}, many=True)
		return Response(status=status.HTTP_200_OK, data=serializer.data)

	@action(detail=True, permission_classes=[IsAuthenticated],
			methods=['post'])
	def follow(self, request, *args, **kwargs):
		user = self.get_object()
		if request.user.follows(user):
			return Response("you already follows this user.", 
						status=status.HTTP_400_BAD_REQUEST)
		request.user.following.add(user)
		user.update_follower_no()
		request.user.update_following_no()
		return Response(status=status.HTTP_200_OK)

	@action(detail=True, permission_classes=[IsAuthenticated],
			methods=['post'])
	def unfollow(self, request, *args, **kwargs):
		user = self.get_object()
		if not request.user.follows(user):
			return Response("you are not following this user.", 
						status=status.HTTP_400_BAD_REQUEST)
		request.user.following.remove(user)
		user.update_follower_no()
		request.user.update_following_no()
		return Response(status=status.HTTP_200_OK)
		
		
class UserInformation(GenericAPIView):
	queryset = User.objects.all()
	serializer_class = UserProfileSerializer
	
	def get(self, request, *args, **kwargs):
		request_user = request.user
		
		try:
			username = request_user.username
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			return Response({'error': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
		
		serializer = UserInformationSerializer(user)
		return Response(serializer.data)
	
	
		
	
	

from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import ModelViewSet

from .filters import ExperienceFilterSet
from .pagination import ExperiencePagination
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.contrib.auth.models import User, AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.db.models import Q
# from accounts.permissions import IsAdmin
from rest_framework.decorators import action


class ExperienceViewSet(ModelViewSet):
	queryset = Experience.objects.all()
	serializer_class = ExperienceSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]
	pagination_class = ExperiencePagination
	filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
	ordering_fields = ['date_created', 'like_number']
	filterset_fields = ['place__title', 'place__contact__city',
				'place__contact__province', 'user__username', 'user__id']
	search_fields = ['title', 'body']
	filterset_class = ExperienceFilterSet
	
	def retrieve(self, request, pk=None):
		# Add field is_owner for retrieve method
  
		# Check if experience exists or not
		try:
			experience = Experience.objects.get(pk=pk)
		except Experience.DoesNotExist:
			return Response({'error': "Experience with given ID does not exist"}, status= status.HTTP_400_BAD_REQUEST)

		serializer = ExperienceSerializer(experience)
		# Check if user is anonymous or not
		if request.user.is_anonymous == False:
			# Get request user, username
			request_user = request.user.username
			request_user.replace(' ', '')
			# Get xp writer usernamme
			xp_user = serializer.data["user_username"]
			xp_user = xp_user.replace(' ', '')
			print(serializer.data["user_username"])
			# Check if xp writer and request user are the same or not
			if request_user == xp_user:
				new_response = {"is_owner":True}    
			else:
				new_response = {"is_owner":False}
		else:
			new_response = {"is_owner":False}
		new_response.update(serializer.data)
		return Response(new_response)


	def update(self, request, *args, **kwargs):
		experience = self.get_object()
		if experience.user.username != request.user.username:
			return Response({'error': "you do not have permission to Edit this experience. Because you're not owner of this experience"}, status=status.HTTP_403_FORBIDDEN)
		else:
			return super().update(request, *args, **kwargs)


	def destroy(self, request, *args, **kwargs):
		experience = self.get_object()
		if experience.user.username != request.user.username:
			return Response({'error': "you do not have permission to Delete this experience. Because you're not owner of this experience"}, status=status.HTTP_403_FORBIDDEN)
		else:
			return super().destroy(request, *args, **kwargs)


	@action(detail=False, permission_classes=[IsAuthenticated])
	def feed(self, request, *args, **kwargs):
		user = request.user
		serializer = ExperienceSerializer(
			user.followers.experiences, many=True)
		return Response(status=status.HTTP_200_OK, data=serializer.data)

 
class LikeViewSet(GenericAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]   
    
    def post(self, request, id, *args, **kwargs):
        user = request.user
        experience = Experience.objects.get(pk=id)
        serializer = LikeSerializer(data=request.data, context = {'experience': experience, 'user': request.user})
        if serializer.is_valid():
            user_likes = Like.objects.filter(user=user, experience=experience)
            if user_likes.exists():
                return Response("You have liked before", status=status.HTTP_400_BAD_REQUEST)
            else:
                experience.like_number += 1
                experience.save()
                serializer.save(user=user, experience=experience)
                return Response(serializer.data, status=status.HTTP_200_OK)
                
    

class CommentViewSet(ModelViewSet):
	queryset = Comment.objects.select_related('experience').all()
	serializer_class = CommentSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get_queryset(self):
		return Comment.objects.filter(
			experience_id=self.kwargs.get('experience_pk'), parent=None)\
			.order_by('-created_date')
	
	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['experience'] = self.kwargs.get('experience_pk')
		return context


	def create(self, request, *args, **kwargs):
		get_object_or_404(Experience.objects, pk=self.kwargs.get('experience_pk'))
		return super().create(request, *args, **kwargs)

	def update(self, request, *args, **kwargs):
		return self.perform_change(request, 'update', *args, **kwargs)

	def destroy(self, request, *args, **kwargs):
		return self.perform_change(request, 'destroy', *args, **kwargs)

	def perform_change(self, request, action, *args, **kwargs):
		user = request.user
		comment = self.get_object()
		experience = comment.experience
		if not comment.is_owner(user):
			return Response('you do not have permission to change this comment.',
							 status=status.HTTP_403_FORBIDDEN)
		if action == 'update':
			return super().update(request, *args, **kwargs)
		response = super().destroy(request, *args, **kwargs)
		experience.update_comment_no()
		return response



class ReplytViewSet(CommentViewSet):
	queryset = Comment.objects.select_related('parent').all()
	serializer_class = ReplySerializer
	http_method_names = ['post', 'put', 'delete']

	def get_queryset(self):
		return Comment.objects.filter(
			Q(experience_id=self.kwargs.get('experience_pk'))&~Q(parent=None))\
			.order_by('-created_date')
	
	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['parent'] = self.kwargs.get('parent_pk')
		return context

	def create(self, request, *args, **kwargs):
		get_object_or_404(Experience.objects, pk=self.kwargs.get('experience_pk'))
		get_object_or_404(Comment.objects, pk=self.kwargs.get('parent_pk'))
		return super().create(request, *args, **kwargs)




				
	
	
	

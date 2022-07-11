from asyncore import read
from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import *
from datetime import datetime

class ExperienceSerializer(serializers.ModelSerializer):
    
    place_title = serializers.SerializerMethodField('get_place_title')
    user_username = serializers.SerializerMethodField('get_user_username')
    user_image = serializers.SerializerMethodField('get_user_image')
    is_liked_new = serializers.SerializerMethodField('get_is_liked')
    
    class Meta:
        model = Experience     
        fields = "__all__"  
        read_only_fields = ['like_number', 'comment_number', 'views', 'rate', 'rate_no', 'place_title', 'user_username', 'user_image', 'user', 'is_liked']
        
    def get_place_title(self, experience):
        place = experience.place
        return place.title
    
    def get_user_username(self, experience):
        user = experience.user
        return user.username
    
    def get_user_image(self, experience):
        user = experience.user
        print(user.image)
        if user.image != "":
            return user.image.url
        else:
            return ""
        
    def get_is_liked(self, experience):
        request = self.context.get("request")
        print(request)
        if request.user.is_anonymous == False:
            user = request.user
        else:
            return False
        
        likes = Like.objects.filter(user=user, experience=experience)
        if len(likes) > 0:
            return True
        else:
            return False
    
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['user'] = request.user
        return super().create(validated_data)
        
        
class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ['user', 'experience']
        
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['user'] = self.context['user']
        validated_data['experience'] = self.context['experience']
        return super().create(validated_data)


class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'image', 'full_name']


class ReplySerializer(serializers.ModelSerializer):
    user = UserCommentSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'created_date', 'text', 'user']
        read_only_fields = ['id', 'created_date', 'user']

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['experience_id'] = self.context.get("experience")
        validated_data['parent_id'] = self.context.get("parent")
        validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['created_date'] = datetime.now()
        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(read_only=True, many=True)
    user = UserCommentSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'created_date', 'text', 'user', 'replies']
        read_only_fields = ['id', 'created_date']

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['experience_id'] = self.context.get("experience")
        validated_data['user'] = request.user
        instance = super().create(validated_data)
        instance.experience.update_comment_no()
        return instance

    def update(self, instance, validated_data):
        validated_data['created_date'] = datetime.now()
        return super().update(instance, validated_data)

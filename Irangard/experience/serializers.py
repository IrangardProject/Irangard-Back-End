from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import *
from datetime import datetime

class ExperienceSerializer(serializers.ModelSerializer):
    
    place_title = serializers.SerializerMethodField('get_place_title')
    user_username = serializers.SerializerMethodField('get_user_username')
    user_image = serializers.SerializerMethodField('get_user_image')
    
    class Meta:
        model = Experience     
        fields = "__all__"  
        read_only_fields = ['like_number', 'comment_number', 'views', 'rate', 'rate_no', 'place_title', 'user_username', 'user_image']
        
    def get_place_title(self, experience):
        place = experience.place
        return place.title
    
    def get_user_username(self, experience):
        user = experience.user
        return user.username
    
    def get_user_image(self, experience):
        user = experience.user
        return user.image.url
        
        
class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Like
        fields = '__all__'


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


class CommentSerializer(ReplySerializer):
    replies = ReplySerializer(read_only=True, many=True)
    class Meta(ReplySerializer.Meta):
        fields = ReplySerializer.Meta.fields + ['replies']

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['experience_id'] = self.context.get("experience")
        validated_data['user'] = request.user
        return serializers.ModelSerializer.create(validated_data)

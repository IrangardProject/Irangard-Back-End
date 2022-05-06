from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import Experience, Like

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

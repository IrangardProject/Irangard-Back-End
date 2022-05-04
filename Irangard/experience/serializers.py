from rest_framework import serializers
from .models import Experience

class ExperienceSerializer(serializers.ModelSerializer):
    
    place_title = serializers.SerializerMethodField('get_place_title')
    user_username = serializers.SerializerMethodField('get_user_username')
    user_image = serializers.SerializerMethodField('get_user_image')
    is_owner = serializers.SerializerMethodField('get_is_owner')
    
    class Meta:
        model = Experience
        fields = "__all__"  
        read_only_fields = ['like_number', 'comment_number', 'views', 'rate', 'rate_no', 'place_title', 'user_username', 'user_image', 'is_owner']
        
    def get_place_title(self, experience):
        place = experience.place
        return place.title
    
    def get_user_username(self, experience):
        user = experience.user
        return user.username
    
    def get_user_image(self, experience):
        user = experience.user
        return user.image.url
    
    def get_is_owner(self, experience):
        request_user = self.context['user']
        if str(request_user) == str(experience.user.username):
            return True
        else:
            return False
        
        
class ExperienceListSerializer(serializers.ModelSerializer):
    
    place_title = serializers.SerializerMethodField('get_place_title')
    user_username = serializers.SerializerMethodField('get_user_username')
    user_image = serializers.SerializerMethodField('get_user_image')
    is_owner = serializers.SerializerMethodField('get_is_owner')
    
    class Meta:
        model = Experience
        exclude = ('body', )
        read_only_fields = ['like_number', 'comment_number', 'views', 'rate', 'place_title', 'user_username', 'user_image', 'is_owner']
        
    def get_place_title(self, experience):
        place = experience.place
        return place.title
    
    def get_user_username(self, experience):
        user = experience.user
        return user.username
    
    def get_user_image(self, experience):
        user = experience.user
        return user.image.url
    
    def get_is_owner(self, experience):
        request_user = self.context['user']
        if str(request_user) == str(experience.user.username):
            return True
        else:
            return False
    
    
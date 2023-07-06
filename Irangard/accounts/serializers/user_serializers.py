from dataclasses import fields
from pyexpat import model
from accounts.models import User, SpecialUser
from rest_framework import serializers
from Irangard.settings import STATIC_HOST


class UserImageUserNameSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')
    class Meta:
        model = User
        fields = ('username', 'id', 'image')
    
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        else:
            return ""


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')

    class Meta:
        model = User
        fields = "__all__"

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        else:
            return ""


class SpecialUserSerializer(serializers.ModelSerializer):
    
    user = UserImageUserNameSerializer(read_only=True)
    class Meta:
        model = SpecialUser
        fields = "__all__"
        
class UserBasicInfoSerializer(serializers.ModelSerializer):
    """Serializer for user basic info """
    class Meta:
        model = User
        fields = ['email', 'username']
   
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    is_owner = serializers.SerializerMethodField('get_is_owner')
    following = serializers.SerializerMethodField('get_following')
    image = serializers.SerializerMethodField('get_image')
    
    
    class Meta:
        model = User
        fields = ['id', 'full_name', 'is_special', 'email', 'image', 'username', 'about_me', 'following_number', 'follower_number', 'following', 'is_owner','is_admin']
        read_only_fields = ('email', 'following_number', 'follower_number', 'is_owner','is_admin')
        
    def get_is_owner(self, user):
        request_user = self.context['user']
        if str(request_user) == str(user.username):
            return True
        else:
            return False

    def get_following(self, user):
        status = None
        request_user = self.context['user']
        if request_user.is_authenticated:
            status =  request_user.follows(user) or request_user == user
        return status
    
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        else:
            return ""


class UserFeedSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField('get_following')

    def get_following(self, user):
        status = None
        request_user = self.context['request'].user
        if request_user.is_authenticated:
            status =  request_user.follows(user) or request_user == user
        return status
    class Meta:
        model = User
        fields = ['id', 'username', 'image', 'full_name', 'following']
        
        
class UserInformationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'


class WhoIsSeriliazer(serializers.Serializer):
    username = serializers.CharField(max_length=50, help_text="user username")

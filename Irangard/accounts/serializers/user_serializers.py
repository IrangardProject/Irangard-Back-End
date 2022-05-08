from accounts.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "all"
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    is_owner = serializers.SerializerMethodField('get_is_owner')
    
    class Meta:
        model = User
        fields = ['full_name', 'is_special', 'email', 'image', 'username', 'about_me', 'following_number', 'follower_number', 'is_owner','is_admin']
        read_only_fields = ('email', 'following_number', 'follower_number', 'is_owner','is_admin')
        
        extra_kwargs = {
        'image': {'read_only': False}
        }
        
        
    def get_is_owner(self, user):
        request_user = self.context['user']
        if str(request_user) == str(user.username):
            return True
        else:
            return False
    
   
        
    
    
    
        


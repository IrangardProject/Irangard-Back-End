from accounts.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    # full_name = serializers.SerializerMethodField('get_fullname')
    
    class Meta:
        model = User
        fields = ['full_name', 'is_special', 'email', 'image', 'username', 'about_me']
        read_only_fields = ('email',)
        
    # def get_fullname(self, user):
    #     first_name = str(user.first_name)
    #     last_name = str(user.last_name)
    #     full_name = first_name + ' ' + last_name
    #     return full_name
    
    # def set_fullname(self, user):
    #     # first_name = str(user.first_name)
    #     # last_name = str(user.last_name)
    #     # full_name = first_name + ' ' + last_name
    #     # return full_name
    #     pass
    
   
        
    
    
    
        


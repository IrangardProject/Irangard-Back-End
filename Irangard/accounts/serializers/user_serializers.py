from accounts.models import User
from rest_framework import serializers

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "all"
        
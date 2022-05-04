from rest_framework import serializers
from .models import Experience

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"
        read_only_fields = ['like_number', 'comment_number', 'views', 'rate', 'rate_no', ]
        
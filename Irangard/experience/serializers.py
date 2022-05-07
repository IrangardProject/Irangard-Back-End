from rest_framework import serializers
from .models import *
from datetime import datetime

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"
        read_only_fields = ['like_number', 'comment_number', 'views', 'rate', 'rate_no', ]


class CommentSerializer(serializers.ModelSerializer):
    reply = ReplySerializer(read_only=True)
    user = UserCommentSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'created_date', 'text', 'user', 'reply']
        read_only_fields = ['id', 'created_date']

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['experience_id'] = self.context.get("experience")
        validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['created_date'] = datetime.now()
        return super().update(instance, validated_data)
        
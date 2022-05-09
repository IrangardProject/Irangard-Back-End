from accounts.models import User
from rest_framework import serializers


class VerifiedPaymentSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    track_id = serializers.IntegerField()
    order_id = serializers.CharField(max_length = 50)
    amount = serializers.IntegerField()
    date = serializers.DateField()
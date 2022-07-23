from accounts.models import User
from rest_framework import serializers


class VerifiedPaymentSerializer(serializers.Serializer):
    status = serializers.IntegerField(read_only=True)
    track_id = serializers.IntegerField(read_only=True)
    order_id = serializers.CharField(read_only=True)
    amount = serializers.IntegerField(read_only=True)
    #date = serializers.DateField(input_formats=)
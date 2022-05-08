from accounts.models import User
from rest_framework import serializers


class VerifiedPaymentSerializer(serializers.Serializer):
    status = serializers.IntegerField(blank=True)
    track_id = serializers.IntegerField(blank = True)
    order_id = serializers.CharField(max_length = 50, blank = True)
    amount = serializers.IntegerField(blank = True)
    date = serializers.DateField(blank = True)
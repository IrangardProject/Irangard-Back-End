from accounts.models import User
from rest_framework import serializers


class VerifiedPaymentSerializer(serializers.Serializer):
    status = serializers.IntegerField(ReadOnly = True)
    track_id = serializers.IntegerField(ReadOnly = True)
    order_id = serializers.CharField(max_length = 50,ReadOnly = True)
    amount = serializers.IntegerField(ReadOnly = True)
    date = serializers.DateField(ReadOnly = True)
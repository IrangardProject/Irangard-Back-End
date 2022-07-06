from accounts.models import *
from rest_framework import serializers


class check_place_ownership_claim_seriliazer(serializers.Serializer):
    
    status_mode = [
        ('AC'),
        ('DN'),
        ('PN'),
    ]
    status = serializers.ChoiceField(choices=status_mode, help_text="place status")
    id = serializers.IntegerField(help_text="place status record id")
    
class StatisticSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()

class MonthlyStatisticResponseSerializer(serializers.Serializer):
    added_monthly_user = serializers.IntegerField()
    added_monthly_special_user = serializers.IntegerField()
    added_monthly_experience = serializers.IntegerField()
    added_monthly_place = serializers.IntegerField()
    added_monthly_tour = serializers.IntegerField()

class WeeklyStatisticResponseSerializer(serializers.Serializer):
    added_weekly_user = serializers.IntegerField()
    added_weekly_special_user = serializers.IntegerField()
    added_weekly_experience = serializers.IntegerField()
    added_weekly_place = serializers.IntegerField()
    added_weekly_tour = serializers.IntegerField()

class DailyStatisticResponseSerializer(serializers.Serializer):
    added_daily_user = serializers.IntegerField()
    added_daily_special_user = serializers.IntegerField()
    added_daily_experience = serializers.IntegerField()
    added_daily_place = serializers.IntegerField()
    added_daily_tour = serializers.IntegerField()


class RemoveUserSerilizer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    
class AddUserSerilizer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
from django_filters.rest_framework import FilterSet
from .models import Tour


class TourFilter(FilterSet):
    
    class Meta:
        model = Tour
        fields = [
            'tour_type', 
            'start_date',
            'end_date', 
            'cost',
            'province',
            'city',
            'owner__user__username',
            'owner__user__id',
        ]
        
        fields = {
            'title': ['contains'], 
            'tour_type': ['exact'], 
            'start_date': ['lte', 'gte'],
            'end_date': ['lte', 'gte'],
            'cost': ['lte', 'gte'],
            'city': ['exact'],
            'province': ['exact'],
            'owner__user__username': ['exact'],
            'owner__user__id': ['exact'],
        }

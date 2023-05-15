from django_filters.rest_framework import FilterSet
from .models import Event
from django_filters import rest_framework as filters


class EventFilter(FilterSet):
    tag = filters.CharFilter(method='filter_by_tag')
    
    class Meta:
        model = Event
        fields = ['province', 'city', 'event_type', 'event_category', 
                'title', 'start_date', 'end_date', 'is_free',
                'added_by__username', 'added_by__id']
        
        
        fields = {
            'title': ['contains'], 
            'event_type': ['exact'],
            'event_category': ['exact'], 
            'start_date': ['lte', 'gte'],
            'end_date': ['lte', 'gte'],
            'is_free': ['exact'],
            'province': ['exact'],
            'city': ['exact'],
            'added_by__username': ['exact'],
            'added_by__id': ['exact']
        }
    
    
    def filter_by_tag(self, queryset, name, value):
        tags = value.split(',')
        return queryset.filter(tags__name__in=tags)

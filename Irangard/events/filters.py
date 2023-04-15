from django_filters.rest_framework import FilterSet
from .models import Event



class EventFilter(FilterSet):
    class Meta:
        model = Event
        fields = ['province', 'city', 'event_type', 'event_category', 
                'tags__name', 'title', 'start_date', 'end_date']
        
        fields = {
            'title': ['contains'], 'event_type': ['exact'], 
            'event_category': ['exact'], 'start_date': ['lte', 'gte'],
            'end_date': ['lte', 'gte'],
        }
    
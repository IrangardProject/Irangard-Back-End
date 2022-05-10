from .models import Experience
from django_property_filter import PropertyFilterSet, PropertyDateFilter

class ExperienceFilterSet(PropertyFilterSet):
    
    class Meta:
        model = Experience
        fields = {
            'place__title': ['contains'], 
            'place__contact__province': ['exact'],
            'place__contact__city': ['exact'],
            'user__username': ['exact'],
            'user__id': ['exact'],
        }
    
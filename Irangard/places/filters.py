from django_filters.rest_framework import FilterSet
from .models import Place
import django_filters
from django_filters import rest_framework as filters


class PlaceFilter(FilterSet):
    province = django_filters.CharFilter(field_name="contact__province", lookup_expr='exact')
    city = django_filters.CharFilter(field_name="contact__city", lookup_expr='exact')
    tag = filters.CharFilter(method='filter_by_tag')
    
    class Meta:
        model = Place
        fields = ['province', 'city', 'place_type', 'is_free', 
                'features__title', 'rooms__capacity']
        
        fields = {
            'rooms__price': ['lte', 'gte'],
            'optional_costs__price': ['lte', 'gte'],
            'rate': ['gte'], 
            'title': ['contains'],
            'place_type': ['exact'],
            'is_free': ['exact'],
        }
    
    def filter_by_tag(self, queryset, name, value):
        return queryset.filter(tags__name=value)

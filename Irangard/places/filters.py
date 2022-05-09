
from django_filters.rest_framework import FilterSet
from .models import Place, Contact
import django_filters




class PlaceFilter(FilterSet):
    province = django_filters.CharFilter(field_name="contact__province", lookup_expr='exact')
    city = django_filters.CharFilter(field_name="contact__city", lookup_expr='exact')

    class Meta:
        model = Place
        fields = ['province', 'city', 'place_type']

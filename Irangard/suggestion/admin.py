from django.contrib import admin
from .models import TourSuggestion, EventSuggestion, PlaceSuggestion


admin.site.register(TourSuggestion)
admin.site.register(EventSuggestion)
admin.site.register(PlaceSuggestion)

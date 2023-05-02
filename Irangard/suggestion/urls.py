from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from .views import TourSuggestionViewSet, EventSuggestionViewSet, PlaceSuggestionViewSet

app_name = 'suggestion'

router = routers.DefaultRouter()
router.register('tour', TourSuggestionViewSet)
router.register('event', EventSuggestionViewSet)
router.register('place', PlaceSuggestionViewSet)


urlpatterns = [
    path('', include(router.urls))
]

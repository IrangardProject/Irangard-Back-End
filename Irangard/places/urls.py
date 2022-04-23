from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import *

app_name = 'places'

router = routers.DefaultRouter()
router.register('', PlaceViewSet)


urlpatterns = [
    path('', include(router.urls))
]

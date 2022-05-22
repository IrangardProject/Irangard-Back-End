from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import *

app_name = 'tours'

router = routers.DefaultRouter()
router.register('', TourViewSet)


urlpatterns = [
    path('', include(router.urls))
]

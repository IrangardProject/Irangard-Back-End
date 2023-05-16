from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from .views import *

app_name = 'events'

router = routers.DefaultRouter()
router.register('', EventViewSet)


urlpatterns = [
    path('', include(router.urls))
]

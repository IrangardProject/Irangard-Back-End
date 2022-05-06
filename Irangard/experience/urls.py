from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import ExperienceViewSet
from django.urls.conf import include


app_name = 'experience'

router = routers.DefaultRouter()
router.register('', ExperienceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('<int:id>/like', LikeViewSet.as_view(), name='like-experience'),
]
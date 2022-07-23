from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import *
from .discount_code_views import *
app_name = 'tours'

router = routers.DefaultRouter()
router.register('', TourViewSet, basename='tours')
dicount_code_router = routers.NestedDefaultRouter(parent_router=router, parent_prefix='', lookup='tour')
dicount_code_router.register('discount-codes', DicountCodeViewSet, basename='tours_discount_codes')



urlpatterns = [
    path('', include(router.urls)),
    path('', include(dicount_code_router.urls))
]

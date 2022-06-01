from unicodedata import name

from django.urls import base, path
from django.urls import re_path, include
from rest_framework_simplejwt import views
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers

from .user_views import *
from .accounts_auth_views import AccountAuthViewSet
from .special_user_views import SpecialUserViewSet
from accounts.serializers.serializersNew import myTokenObtainPairSerializer
from .admin_views import AdminViewSet
from .views import PayViewSet

app_name = 'accounts'

router =  routers.DefaultRouter()
router.register('auth', AccountAuthViewSet,
                basename='accounts-auth')
router.register('pay',PayViewSet , basename='accounts-pay')
router.register('admin', AdminViewSet, basename='accounts-admin')
router.register('', FeediewSet)
router.register('special-users', SpecialUserViewSet, basename='special-users')

urlpatterns = [
    path('',include(router.urls)),
    path('profile/<username>/', UserProfile.as_view(), name='user-profile'),
    path('information', UserInformation.as_view(), name='user-information'),
    path("auth/jwt/create", views.TokenObtainPairView.as_view(serializer_class=myTokenObtainPairSerializer),
            name="accounts-jwt-create"),
    path("auth/jwt/refresh", views.TokenRefreshView.as_view(),
            name="accounts-jwt-refresh"), 
    path("auth/jwt/verify", views.TokenVerifyView.as_view(),
            name="accounts-jwt-verify"),
#     path(r'^jwt/token/?', views.TokenObtainPairView.as_view(serializer_class=myTokenObtainPairSerializer), name='accounts-jwt-token-new'),
]

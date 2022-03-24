from django.urls import base, path
from django.urls import re_path, include
from rest_framework_simplejwt import views
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers
from .accounts_auth import AccountAuthViewSet
from .views import *

app_name = 'accounts'

router =  routers.DefaultRouter()
router.register('auth', AccountAuthViewSet,
                basename='accounts-auth')

urlpatterns = [
    path('',include(router.urls)),
    path("auth/jwt/create", views.TokenObtainPairView.as_view(),
            name="accounts-jwt-create"),
    path("auth/jwt/refresh", views.TokenRefreshView.as_view(),
            name="accounts-jwt-refresh"),
    path("auth/jwt/verify", views.TokenVerifyView.as_view(),
            name="accounts-jwt-verify"),
]


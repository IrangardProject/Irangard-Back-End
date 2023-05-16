from unicodedata import name

from django.urls import base, path
from django.urls import re_path, include
from rest_framework_simplejwt import views
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers
from . import user_views
from .user_views import *
from .accounts_auth_views import AccountAuthViewSet
from .special_user_views import SpecialUserViewSet
from accounts.serializers.serializersNew import myTokenObtainPairSerializer
from .admin_views import AdminViewSet
from .views import PayViewSet
from .views import *
from accounts.user_views import FollowViewSet

app_name = 'accounts'

router =  routers.DefaultRouter()
router.register('auth', AccountAuthViewSet,
                basename='accounts-auth')
router.register('pay',PayViewSet , basename='accounts-pay')
router.register('admin', AdminViewSet, basename='accounts-admin')
router.register('special-users', SpecialUserViewSet, basename='special-users')
router.register('wallet', WalletViewSet, basename='wallet')
router.register('', FollowViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('profile/<username>', UserProfile.as_view(), name='user-profile'),
    path('information', UserInformation.as_view(), name='user-information'),
    path('chat-users', ChatUsers.as_view(), name='chat-users'),
    path('user-rooms/<int:pk>', UserMessageRooms.as_view(), name='user-rooms'),
    path('claimed-places', ClaimedPlaceOwnership.as_view(), name='user-claimed_places'),
    path('who-is', WhoIs.as_view(), name='user-who-is'),
    path('users', GetAllUsers.as_view(), name='user-all'),
    path("auth/jwt/create", views.TokenObtainPairView.as_view(serializer_class=myTokenObtainPairSerializer),
            name="accounts-jwt-create"),
    path("auth/jwt/refresh", views.TokenRefreshView.as_view(),
            name="accounts-jwt-refresh"), 
    path("auth/jwt/verify", views.TokenVerifyView.as_view(),
            name="accounts-jwt-verify"),
#     path(r'^jwt/token/?', views.TokenObtainPairView.as_view(serializer_class=myTokenObtainPairSerializer), name='accounts-jwt-token-new'),
]

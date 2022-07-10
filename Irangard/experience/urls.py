from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import *
from django.urls.conf import include


app_name = 'experience'

router = routers.DefaultRouter()
router.register('', ExperienceViewSet)
experiences_router = routers.NestedDefaultRouter(
    parent_router=router, parent_prefix='', lookup='experience')  # experience_pk
experiences_router.register('comments', CommentViewSet, basename='experience-comments')

comments_router = routers.NestedDefaultRouter(
    parent_router=experiences_router, parent_prefix='comments', lookup='parent')  # comment_pk
comments_router.register('reply', ReplytViewSet, basename='reply')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>/like', LikeViewSet.as_view(), name='like-experience'),
    path('<int:id>/unlike', UnLikeViewSet.as_view(), name='unlike-experience'),
    path('', include(experiences_router.urls)),
    path('', include(comments_router.urls)),
]
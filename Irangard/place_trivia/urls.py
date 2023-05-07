from django.urls import path
from .views import PlaceTriviaAPIView


urlpatterns = [
    path('', PlaceTriviaAPIView.as_view(), name='place-trivia-view'),
    path('province/<str:province>/', PlaceTriviaAPIView.as_view(), name='place-trivia-view'),
    path('city/<str:city>/', PlaceTriviaAPIView.as_view(), name='place-trivia-view'),
]

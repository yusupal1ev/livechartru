from django.urls import path
from .views import HomeView, SeasonView


urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('season/<str:season>-<int:year>', SeasonView.as_view(), name='season'),
]

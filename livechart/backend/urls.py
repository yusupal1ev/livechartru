from django.urls import path
from .views import HomeView, RefreshView


urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('refresh/', RefreshView.as_view(), name='refresh'),
]

from django.urls import path
from .views import HomeView, SeasonView, CrawlerView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('season/<str:season>-<int:year>', SeasonView.as_view(), name='season'),
    path('crawler/', CrawlerView.as_view(), name='crawler')
]

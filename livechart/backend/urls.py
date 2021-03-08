import debug_toolbar

from django.urls import path, include

from .views import HomeView, SeasonView, CrawlerView, AnimeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('season/<str:season>-<int:year>', SeasonView.as_view(), name='season'),
    path('anime/<int:data_id>', AnimeView.as_view(), name='anime'),
    path('crawler/', CrawlerView.as_view(), name='crawler'),

    path('__debug__/', include(debug_toolbar.urls)),
]

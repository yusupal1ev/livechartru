import debug_toolbar

from django.urls import path, include

from .views import HomeView, SeasonView, CrawlerView, TitleView, CategoryView, StudioView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('season/<str:season>-<int:year>', SeasonView.as_view(), name='season'),
    path('category/<str:category>', CategoryView.as_view(), name='category'),
    path('studio/<str:studio>', StudioView.as_view(), name='studio'),
    path('anime/<int:data_id>', TitleView.as_view(), name='title'),
    path('crawler/', CrawlerView.as_view(), name='crawler'),

    path('__debug__/', include(debug_toolbar.urls)),
]

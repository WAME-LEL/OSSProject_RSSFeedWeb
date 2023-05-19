# from django.urls import path
# from .views import LatestPostsFeed
# from . import views
#
# urlpatterns = [
#     path('feed/', LatestPostsFeed(), name='post_feed')
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.rss_feed,name='rss_feed'),
    path('sub/',views.sub,name='sub'),
    path('LatestEntriesFeed/', views.LatestEntriesFeed, name='LatestEntriesFeed'),
]
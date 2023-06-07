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
    path('test/',views.sublist,name='sublist'),
    path('RSS_Del/<int:subsData_id>/', views.RSS_Del, name='RSS_Del'),
    path('Sub_cate/<int:ob_id>/',views.Sub_cate,name='Sub_cate'),
    path('scrap/', views.scrap, name='scrap'),
    path('scrapSave/',views.scrapSave,name='scrapSave'),
    path('scrap_Del/<int:scrap_item_id>/',views.scrap_Del,name='scrap_Del'),
]
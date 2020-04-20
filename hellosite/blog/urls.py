from django.urls import path
from blog.sitemaps import PostMaps
from . import views
from django.contrib.sitemaps.views import sitemap
from blog.feed import LatestPostsFeed

app_name = 'blog'

sitemaps = {'posts': PostMaps, }
urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('feed/', LatestPostsFeed(), name='post_feed'),

]
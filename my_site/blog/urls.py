from django.conf.urls import url
from . import views
from .feeds import LatestPostsFeed


app_name = 'blog'

# Create URL mappings here
urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    # url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', views.post_detail, name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.share_post, name='share_post'),
    url(r'^feed/$', LatestPostsFeed(), name='post_feed'),
]
from django.conf.urls import url
from .views import user_login, dashboard


app_name = "bookmarks"

urlpatterns = [
    url(r'^$', user_login, name='user_login'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
]

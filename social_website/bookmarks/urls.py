from django.conf.urls import url
from django.contrib.auth.views import (login,
                                       logout,
                                       logout_then_login,
                                       password_change,
                                       password_change_done,
                                       password_reset,
                                       password_reset_confirm,
                                       password_reset_done,
                                       password_reset_complete)
from django.views.generic import TemplateView
from .views import dashboard, register


app_name = "bookmarks"

urlpatterns = [
    # Login URLs
    url(r'^login/$',
        login,
        name='login'),
    url(r'^logout/$',
        logout,
        name='logout'),
    url(r'^logout-then-login/$',
        logout_then_login,
        name='logout_then_login'),
    # Dashboard URLs
    url(r'^$',
        dashboard,
        name='dashboard'),
    url(r'^about_me/$',
        TemplateView.as_view(template_name="about_me.html"),
        {'section': 'about_me'},
        name="about_me"),
    # Change Password URLs
    url(r'^password-change/$',
        password_change,
        name='password_change'),
    url(r'^password-change/done/$',
        password_change_done,
        name='password_change_done'),
    # Reset Password URLs
    url(r'^password-reset/$',
        password_reset,
        name='password_reset'),
    url(r'^password-reset/done/$',
        password_reset_done,
        name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$',
        password_reset_complete,
        name='password_reset_complete'),
    url(r'^register/$',
        register,
        name='register'),
]

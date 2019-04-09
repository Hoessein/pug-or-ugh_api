from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from . import views

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', views.UserRegisterView.as_view(), name='register-user'),
    # url(r'^api/dog/(?P<pk>\d+)/liked/next/$', views.ListUndecidedDogs.as_view(), name='liked-dogs'),
    url(r'^api/user/preferences/$', views.UserPreferences.as_view(), name='user-detail'),
    # url(r'^api/dog/(?P<pk>\d+)/liked/next/$', views.ListUndecidedDogs.as_view(), name='liked-dogs'),
    url(r'^api/dog/(?P<pk>\d+)/undecided/next/$', views.ListDogs.as_view(), name='undecided-dogs'),
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),

    #
    # url(r'^$'/api/undecided, views.ListDog.as_view(), name='dog_list'),
    #
    # url(r'^api/dog/(?P<pk>\d+)/liked/next/$',
    #     views.RetrieveUpdateDestroyDog.as_view(),
    #     name='dog_detail'),

    url(r'^$', TemplateView.as_view(template_name='index.html'))
])

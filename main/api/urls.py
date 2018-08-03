

from main.api.views import *
from rest_framework import renderers

from django.conf.urls import url, include

urlpatterns = [
    url(r'^profile_page/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='profile_page'),
    url(r'^party_membership/(?P<pk>[0-9]+)/$', PartyMembershipsCreateDelete.as_view(), name='party_memberships_created_elete'),
    url(r'^list_movies/$', MovieListAPIView.as_view(), name='list_movies'),
    url(r'^list_rated_movies/$', RatingMovieListAPIView.as_view(), name='list_rated_movies'),
   
    # url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
    # url(r'^$', api_root),
    # url(r'^snippets/$', views.SnippetList.as_view(), name='snippet-list'),
    # url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(), name='snippet-detail'),
    # url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view(),  name='snippet-highlight'),
    # url(r'^users/$', views.UserList.as_view(), name='user-list'),
    # url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),

    # url(r'^snippets/$', snippet_list, name='snippet-list'),
    # url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
    # url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
    # url(r'^users/$', user_list, name='user-list'),
    # url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
]
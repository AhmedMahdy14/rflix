from main.api.views import *
from rest_framework import renderers
from django.conf.urls import url, include

urlpatterns = [
    url(r'^movie/create/$', MovieCreate.as_view(), name='create_movie'),
    url(r'^movie/delete/(?P<pk>[0-9]+)/$', MovieDelete.as_view(), name='delete_movie'),
    url(r'^movies/$', MovieList.as_view(), name='list_movies'),
    url(r'^movie/detail/(?P<pk>[0-9]+)/$', MovieDetail.as_view(), name='retrieve_movie'),
    url(r'^movie/edit/(?P<pk>[0-9]+)/$', MovieCreate.as_view(), name='edit_movie'),
    url(r'^movie/recommendations$', MovieRecommendation.as_view(), name='list_movies_recommended'),
    url(r'^movie/rate/create/(?P<pk>[0-9]+)/$', MovieRateCreate.as_view(),
        name='create_rate_movie'),
    url(r'^movie/rate/edit/(?P<pk>[0-9]+)/$', MovieRateEdit.as_view(), name='edit_rate_movie'),
    url(r'^profile_page/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='profile_page'),
    url(r'^user/create/$', UserCreate.as_view(), name='create_user'),
    url(r'^user/delete/(?P<pk>[0-9]+)/$', UserDelete.as_view(), name='delete_user'),
    url(r'^users/$', UserList.as_view(), name='list_users'),
    url(r'^user/detail/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='retrieve_movie'),
    url(r'^user/edit/(?P<pk>[0-9]+)/$', UserEdit.as_view(), name='edit_user'),
    url(r'^party/create/$', PartyCreate.as_view(), name='create_party'),
    url(r'^party/delete/(?P<pk>[0-9]+)/$', PartyDelete.as_view(), name='delete_party'),
    url(r'^party/$', PartyList.as_view(), name='list_parties'),
    url(r'^party/detail/(?P<pk>[0-9]+)/$', PartyDetail.as_view(), name='retrieve_party'),
    url(r'^party/edit/(?P<pk>[0-9]+)/$', PartyEdit.as_view(), name='edit_party'),
    url(r'^party/leave/(?P<pk>[0-9]+)/$', PartyLeave.as_view(), name='leave_party'),
    url(r'^party/join/(?P<pk>[0-9]+)/$', PartyJoin.as_view(), name='join_party'),
]

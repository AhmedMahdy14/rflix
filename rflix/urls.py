"""rflix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include


from main import views
# from main.api import urls as api_url
urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('movies/', views.movies, name='movies'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile_page/', views.profile_page_view, name='profile_page'),
    path('personalized_recommendation_page/', views.personalized_recommendation_page, name='personalized_recommendation_page'),
    path('list_parties/', views.list_parties, name='list_parties'),
    path('party_detail/<int:id>/', views.party_detail, name='party_detail'),
    path('create_party/', views.create_party, name='create_party'),
    path('reporting_page/', views.reporting_page, name='reporting_page'),
    path('leave_party/', views.leave_party, name='leave_party'),
    path('join_party/', views.join_party, name='join_party'),
    path('delete_rating/<int:movie_id>/', views.delete_rating, name='delete_rating'),
    url(r'^api/', include('main.api.urls')),    

]


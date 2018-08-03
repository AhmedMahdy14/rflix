from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from main.models import *
from main.api.serializers import *


from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


from django.http import Http404
from rest_framework.views import APIView


from rest_framework import mixins
from rest_framework import generics

from django.contrib.auth.models import User

from rest_framework import permissions
from main.api.permissions import *

from rest_framework.reverse import reverse

from rest_framework import renderers

from rest_framework.decorators import action

from rest_framework import viewsets

from rest_framework.permissions import *
from main.api.serializers import *
from main.api.permissions import *




class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)




class PartyMembershipsCreateDelete(generics.CreateAPIView, generics.DestroyAPIView,generics.RetrieveAPIView):
    # obj = Party.objects.all()
    queryset = Party.objects.all()
    serializer_class = PartyMembershipsSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)



# @permission_classes((IsAuthenticated, ))
# @api_view(['GET'])
# def list_movies(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     try:
#         movie_type = request.GET['type']
#         movies = set(RatingMovie.objects.filter(user=request.user.pk))
#         if movie_type == 'rated':
#             pass
#         elif movie_type == 'unrated':
#             movies = set(Movie.objects.all()) - movies
#         else:
#             raise ValueError('You have to set either rated or unrated.')
#     except Exception as e:
#         raise e

#     serializer = MoviesSerializer(movies, many=True)
#     return Response(serializer.data)


from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     RetrieveUpdateAPIView, UpdateAPIView)
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from main.api.paginations import *

class MovieListAPIView(ListAPIView):
    serializer_class = MovieSerializer
    pagination_class = PostPageNumberPagination#PostOffsetLimitPagination
    permission_classes = [IsAuthenticated]
    ordering = ('title')

    def get_queryset(self, *args, **kwargs): 
        queryset_list = RatingMovie.objects.all()
        query = self.request.GET.get('type')
        try:
            query = self.request.GET['type']
            queryset_list = {rating_obj.movie for rating_obj in RatingMovie.objects.filter(user=self.request.user.pk)}
            if query == 'rated':
                pass
            elif query == 'unrated':
                queryset_list = set(Movie.objects.all()) - queryset_list
            else:
                raise ValueError('You have to set either rated or unrated in the query.')
        except Exception as e:
            raise e

        return list(queryset_list)    



class RatingMovieListAPIView(ListAPIView):
    serializer_class = RatingMoviesSerializer
    pagination_class = PostPageNumberPagination
    permission_classes = [IsAuthenticated]
    queryset = RatingMovie.objects.all()

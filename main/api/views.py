from django.http import Http404
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from main.api.permissions import  *
from main.api.paginations import *
from main.api.serializers import *
from rest_framework.response import Response
from collections import defaultdict


class MovieCreate(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (permissions.IsAdminUser, )


class MovieDelete(generics.DestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)


class MovieList(generics.ListAPIView):
    serializer_class = MovieSerializer
    pagination_class = MyPagination
    permission_classes = (permissions.IsAuthenticated, )
    ordering = ('rated_by', )
    queryset = Movie.objects.all()

    def get_queryset(self, *args, **kwargs): 
        query = self.request.GET.get('type')
        if query:
            queryset_list = {rating_obj.movie for rating_obj in
                             RatingMovie.objects.filter(user=self.request.user.pk)}
            if query == 'rated':
                pass
            elif query == 'unrated':
                queryset_list = set(Movie.objects.all()) - queryset_list
            else:
                raise Http404
                # raise ValueError('You have to set a type field to either rated or unrated.')
        else:
            queryset_list = Movie.objects.all()
            # raise ValueError('You have to set a type field to either rated or unrated.')

        return list(queryset_list)


class MovieDetail(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (permissions.IsAuthenticated, )


class MovieRecommendation(generics.ListAPIView):
    serializer_class = MovieRecommendationSerializer
    pagination_class = MyPagination
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Movie.objects.all()

    def get_queryset(self, *args, **kwargs): 
        user = self.request.user
        # grab all rated movies by this user to exclude it from recommended movies
        rated_movies_qs = RatingMovie.objects.filter(user=user)
        unrecommended_movies = {
            rated_movie.movie for rated_movie in rated_movies_qs}
        # override rated_movies_qs to get only movies which have high rate.
        rated_movies_qs = rated_movies_qs.filter(p_rating__range=(3, 5))
        user_clan = []
        recommendations = []
        recommendations_dict = defaultdict(dict)
        if rated_movies_qs.count() > 0:
            for query in rated_movies_qs:
                user_clan += RatingMovie.objects.filter(movie=query.movie, p_rating__range=(3, 5))\
                    .exclude(user=user).values_list('user')
            # Grab all movies' clan which have rating at least 3.
            if user_clan:
                for user_query in user_clan:
                    recommendations += RatingMovie.objects.filter(user=user_query,
                                                                  p_rating__range=(3, 5))\
                        .exclude(movie__in=unrecommended_movies)

                movies_temp = set()
                for obj in recommendations:
                    if obj.movie not in movies_temp:
                        movies_temp.add(obj.movie)
                        recommendations_dict[obj.movie]['clan_rating'] = obj.p_rating
                        recommendations_dict[obj.movie]['n_raters'] = 1
                    else:
                        n_raters = recommendations_dict[obj.movie]['n_raters']
                        recommendations_dict[obj.movie]['clan_rating'] = \
                            (obj.p_rating * n_raters + obj.p_rating) * (n_raters + 1)
                        recommendations_dict[obj.movie]['n_raters'] = n_raters + 1
                        
                if recommendations_dict:
                    recommendations_dict = sorted(
                        recommendations_dict.items(),
                        key=lambda item: item[1]['clan_rating'], reverse=True)[:5]
                    recommendations_dict = [ movie[0] for movie in recommendations_dict]
            else:
                recommendations = Movie.objects.all().exclude(pk__in=[movie.pk for movie\
                in unrecommended_movies]).order_by('-rating', 'title')[:5]

        else:
            recommendations = Movie.objects.all().order_by('-rating', 'title')[:5]

        return recommendations_dict if recommendations_dict else recommendations


class MovieRateEdit(generics.UpdateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieRateSerializer
    permission_classes = (permissions.IsAuthenticated, IsMovieRaterOwner)

    def perform_update(self, serializer):
        user = self.request.user
        serializer = serializer.save()
        rm_obj = RatingMovie.objects.get(movie=serializer, user=user)
        rm_obj.p_rating = serializer.p_rating
        rm_obj.save()


class MovieRateCreate(generics.CreateAPIView):
    queryset = RatingMovie.objects.all()
    serializer_class = MovieRateSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        p_rating = request.data.get('p_rating')
        movie = Movie.objects.filter(id=kwargs['pk']).first()
        if not movie:
            return Http404
        user = self.request.user
        if RatingMovie.objects.filter(movie=movie, user=user).count() == 0:
            movie.rating = (movie.rating * movie.nratings + float(p_rating)) /\
                           (movie.nratings + 1)
            movie.nratings += 1
            RatingMovie.objects.create(user=user, movie=movie, p_rating=p_rating)
            movie.save()
            return Response(status=204)
        else:
            return Response(status=404)


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )


class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = MyPagination
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
    ordering = ('id',)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerorAdmin)


class UserEdit(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerorAdmin)


class PartyCreate(generics.CreateAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        party_obj = serializer.save()
        party_obj.n_members = 1
        party_obj.party_memberships.add(self.request.user)
        party_obj.save()


class PartyDelete(generics.DestroyAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    permission_classes = (permissions.IsAuthenticated, IsPartyOwnerorAdmin)


class PartyList(generics.ListAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    pagination_class = MyPagination
    permission_classes = (permissions.IsAuthenticated,)


class PartyDetail(generics.RetrieveAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    permission_classes = (permissions.IsAuthenticated, )


class PartyEdit(generics.UpdateAPIView):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    permission_classes = (permissions.IsAuthenticated, IsPartyOwnerorAdmin)


class PartyLeave(generics.UpdateAPIView):
    queryset = Party.objects.all()
    serializer_class = PartyJoinorLeaveSerializer
    permission_classes = (permissions.IsAuthenticated, IsPartyOwnerorAdmin)

    def perform_update(self, serializer):
        party_obj = serializer.save()
        user =  self.request.user 
        if user in party_obj.party_memberships.all():
            party_obj.party_memberships.remove(user)
            party_obj.n_members -= 1
            party_obj.save()
        else:
            party_obj.n_members += 1
            party_obj.party_memberships.add(user)


class PartyJoin(generics.UpdateAPIView):
    queryset = Party.objects.all()
    serializer_class = PartyJoinorLeaveSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_update(self, serializer):
        party_obj = serializer.save()
        user =  self.request.user 
        if user not in party_obj.party_memberships.all() and party_obj.n_members < 10:
            party_obj.n_members += 1
            party_obj.party_memberships.add(user)
            party_obj.save()

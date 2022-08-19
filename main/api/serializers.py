from rest_framework import serializers
from main.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        order_by = ('id', )

class RatingMovieSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = RatingMovie
        fields = ('user_id', 'name', 'p_rating')


# it is used for list, create, retrieve and delete endpoints  movies 
class MovieSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='api:rated_movie_detail')
    # those  fields would could not be accessed while creating new movie instance by admin.
    p_rating = RatingMovieSerializer(source='ratingmovie_set', many=True)
    rating = serializers.FloatField(max_value=5, min_value=0, read_only=True,  default=0)
    nratings = serializers.IntegerField(default=0, read_only=True)
    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'rating', 'nratings', 'p_rating')
        # order_by = ('title', )

# used only to recommend some movies, so you don't need to show p_rating 
class MovieRecommendationSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='api:rated_movie_detail')
    # those  fields would could not be accessed while creating new movie instance by admin.
    # p_rating = RatingMovieSerializer(source='ratingmovie_set', many=True)
    rating = serializers.FloatField(max_value=5, min_value=0, read_only=True,  default=0)
    nratings = serializers.IntegerField(default=0, read_only=True)
    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'rating', 'nratings', )
        # order_by = ('title', )

class MovieRateSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='api:rated_movie_detail')
    # those  fields would could not be accessed while creating new movie instance by admin.
    # p_rating = RatingMovieSerializer(source='ratingmovie_set', many=True)
    # rating = serializers.FloatField(max_value=5, min_value=0, read_only=True,  default=0)
    # nratings = serializers.IntegerField(default=0, read_only=True)
    class Meta:
        model = RatingMovie
        fields = ('p_rating', )
        # order_by = ('title', )

class MovieRateEditSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='api:rated_movie_detail')
    # those  fields would could not be accessed while creating new movie instance by admin.
    # p_rating = RatingMovieSerializer(source='ratingmovie_set', many=True)
    # rating = serializers.FloatField(max_value=5, min_value=0, read_only=True,  default=0)
    # nratings = serializers.IntegerField(default=0, read_only=True)
    class Meta:
        model = RatingMovie
        fields = ('p_rating', )
        # order_by = ('title', )


# class PartyMembershipSerializer(serializers.HyperlinkedModelSerializer):
#     user_id = serializers.ReadOnlyField(source='user.id')
#     name = serializers.ReadOnlyField(source='user.username')
#     class Meta:
#         model = Party.party_memberships
#         fields = ('user_id', 'name', 'p_rating')


class PartySerializer(serializers.ModelSerializer):
    party_memberships = UserSerializer(read_only=True, many=True)
    n_members = serializers.IntegerField(read_only=True)
    class Meta:
        model = Party
        fields = ('id', 'n_members', 'name', 'party_memberships')

class PartyJoinorLeaveSerializer(serializers.ModelSerializer):
    # party_memberships = UserSerializer(read_only=True, many=True)
    # n_members = serializers.IntegerField(read_only=True)
    class Meta:
        model = Party
        fields = ('id',)

from rest_framework import serializers
from main.models import *



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class PartyMembershipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Party.party_memberships
        fields = ('id',)


class PartySerializer(serializers.ModelSerializer):
    party_memberships = PartyMembershipsSerializer(read_only=True, many=True)
    class Meta:
        model = Party
        fields = ('id', 'n_members', 'email')


class RatingMoviesSerializer(serializers.ModelSerializer):
    # party_memberships = PartyMembershipsSerializer(read_only=True, many=True)
    # def get_user(self, obj):
    #     # obj is model instance
    #     return obj.user.username

    class Meta:
        model = RatingMovie
        fields = ( 'user',)


class MovieSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='api:rated_movie_detail')
    rated_by = RatingMoviesSerializer(read_only=True, many=True)
    class Meta:
        model = Movie
        fields = ( 'title', 'year', 'rating', 'nratings', 'rated_by')
        # order_by = ('title', )
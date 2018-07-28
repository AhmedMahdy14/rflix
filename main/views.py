from django.shortcuts import render, redirect, get_object_or_404
from main.models import Movie
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm, PersonalizedRating
from django import forms
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    )
from django.db.models import Q
from .models import  *
from copy import deepcopy
import operator 
from  collections import *
def index(request):

    request.session.set_expiry(1800) 
    return render(request, 'index.html')


def movies(request):
    if not request.user.is_authenticated :
        return redirect("/login")
    request.session.set_expiry(1800) 
    form = PersonalizedRating(request.POST or None)
    if form.is_valid():
        
        new_rating =  form.save(commit=False) 
        new_rating.save()
        return redirect("/movies")

    all_movies = {movie_obj for movie_obj in   Movie.objects.all()}
    rated_movies = {rating_obj.movie:rating_obj.p_rating for rating_obj in RatingMovie.objects\
    .filter(user=request.user.pk)}
    unrated_movies = all_movies - set(rated_movies.keys())
    context = {'rated_movies': rated_movies, 'unrated_movies': unrated_movies, 'form':form}
    return render(request, 'movies.html', context)


def personalized_recommendation_page(request):
    if not request.user.is_authenticated :
        return redirect("/login")
    request.session.set_expiry(1800) 
    user = request.user
    rated_movies_qs = RatingMovie.objects.filter(user=user)
    unrecommended_movies = {rated_movie.movie for rated_movie in  rated_movies_qs}
    rated_movies_qs = rated_movies_qs.filter(p_rating__range=(3,5))
    user_clan = []
    recommendations = []
    recommendations_dict =  [] 
    if rated_movies_qs:
        for query in rated_movies_qs:
            user_clan += RatingMovie.objects.filter(movie=query.movie, p_rating__range=(3,5))\
            .exclude(user=user).values_list('user')
        # Grab all movies clan which have rating at least 3. 
        if user_clan:
            for user_query in user_clan:
                recommendations += RatingMovie.objects.filter(user=user_query, p_rating__range=(3,5))\
                .exclude(movie__in=unrecommended_movies)

            movies_temp = set()
            for obj in recommendations:
                if obj.movie not in movies_temp:
                    movies_temp.add(obj.movie)
                    temp = {}
                    temp['movie'] = obj.movie.title
                    temp['users'] = {rated_movie_obj.user.pk : rated_movie_obj.p_rating for rated_movie_obj in recommendations if rated_movie_obj.movie == obj.movie}
                    temp['clan_rating'] = sum(temp['users'].values()) / len(temp['users'])
                    recommendations_dict.append(deepcopy(temp))
            if recommendations_dict:
                recommendations_dict = sorted(recommendations_dict, key=lambda item: item['clan_rating'], reverse=True)
                # recommendations_dict = sorted(recommendations_dict, key=attrgetter('clan_rating','movie'), reverse=True)
            if len(recommendations_dict) >5:
                recommendations_dict = recommendations_dict[:5]            
        else:
            recommendations = Movie.objects.all().exclude(pk__in=[movie.pk for movie in unrecommended_movies])\
            .order_by('-rating', 'title')
            if len(recommendations) > 5:
                recommendations = recommendations[:5]

    else:
        recommendations = Movie.objects.all().order_by('-rating','title')
        if len(recommendations) > 5:
            recommendations = recommendations[:5]

    context = {'recommendation':recommendations, 'recommendations_dict':recommendations_dict}
    return render(request, "recommendation.html", context)

def list_parties(request):
    if not request.user.is_authenticated :
        return redirect("/login")
    request.session.set_expiry(1800) 
    user = request.user
    all_parties = set(Party.objects.all())
    joined_parties = set(Party.objects.filter(party_memberships=user))
    unjoined_parties =  all_parties - joined_parties
    context = {'joined':joined_parties, 'unjoined':unjoined_parties}
    return render(request, 'list_parties.html', context)

def create_party(request):
    if not request.user.is_authenticated :
            return redirect("/login")
    request.session.set_expiry(1800) 
    user = request.user
    obj = Party()
    obj.save()
    obj.n_members = 1
    obj.party_memberships.add(user)
    obj.save()
    return redirect('/list_parties')

def party_detail(request, id=None):
    if not request.user.is_authenticated :
            return redirect("/login")
    request.session.set_expiry(1800) 
    obj = get_object_or_404(Party, id=id)
    members = obj.party_memberships.all().order_by('username')
    rated_movies = []
    for member in members:
        rated_movies += list(RatingMovie.objects.filter(user=member))
    #party_rating = {movie_instance : [number_of_users, summation of p_rating, global rating]}
    party_rating = []
    for obj1  in rated_movies:
        if obj1.movie not in party_rating :
            party_rating[obj1.movie] = [1] 
            party_rating[obj1.movie].append(obj1.p_rating)
            party_rating[obj1.movie].append(obj1.movie.rating)
            for obj2 in rated_movies:
                if obj1 != obj2 and obj1.movie == obj2.movie:
                    party_rating[obj1.movie][0] += 1 
                    party_rating[obj1.movie][1] += obj2.p_rating

    for key, value in party_rating.items():
        party_rating[key][0] = value[1] / value[0]
        del party_rating[key][1]

    sorted_party_rating = sorted(party_rating.items(), key=lambda x:x[1][0], reverse=True)
    del party_rating
    if len(sorted_party_rating) > 5:
        sorted_party_rating = sorted_party_rating[:5]
    
    title = 'Party Detail'
    context = {'title':title, 'members':members, 'party_rating':sorted_party_rating}
    return render(request, 'party_detail.html', context)


def reporting_page(request):
    if not request.user.is_authenticated :
            return redirect("/login")
    request.session.set_expiry(1800) 
    n_movies = Movie.objects.count()
    n_users = User.objects.count()
    n_ratings = RatingMovie.objects.count()
    # total_ratings = sum([rating[0] for rating in Movie.objects.all().values_list('rating')])
    ratings_per_movie = n_ratings / n_movies
    ratings_per_user = n_ratings / n_users

    user_number_of_ratings = {}
    rated_movies = RatingMovie.objects.all().order_by('username')
    for obj1  in rated_movies:
        if obj1.user not in user_number_of_ratings :
            user_number_of_ratings[obj1.user] = 1
            for obj2 in rated_movies:
                if obj1 != obj2 and obj1.user == obj2.user:
                    user_number_of_ratings[obj1.user] += 1 


    sorted_user_number_of_ratings = sorted(user_number_of_ratings.items(), key=lambda x:x[1], reverse=True)
    del user_number_of_ratings
    if len(sorted_user_number_of_ratings) > 10:
        sorted_user_number_of_ratings = sorted_user_number_of_ratings[:10]


    n_parties = Party.objects.count()
    total_users_in_parties = sum(party.n_members for party in Party.objects.all())
    users_per_party = total_users_in_parties / n_parties

    

def register_view(request):
    request.session.set_expiry(1800) 
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user =  form.save(commit=False) #user instance
        password = form.cleaned_data.get('password') #get actual password from the form
        user.set_password(password)
        user.is_staff = True
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect("/")
        # return render(request, 'index.html')

    context = {
        "form": form,
        "title": title
    }
    return render(request, "form.html", context)



def login_view(request):
    request.session.set_expiry(1800) 
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user) #here to be actually loged in
        return redirect("/profile_page")
    return render(request, "form.html", {"form":form, "title": title})



def profile_page_view(request):
    request.session.set_expiry(1800) 
    title = "Profile Page"
    username = request.user.username
    email    =  request.user.email
    context = {
        "username": username,
        "email":email,
        "title": title
    }
    return render(request, "profile_page.html", context)



def logout_view(request):
    logout(request)
    return redirect("/")
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.urls import reverse

class Movie(models.Model):
    title    = models.CharField(max_length=150)
    year     = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2200)],
                                   default=timezone.datetime.now().year)
    #global rating
    rating   = models.FloatField( validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    nratings = models.PositiveIntegerField(default=0)
    rated_by    = models.ManyToManyField(User, through='RatingMovie')

    def __str__(self):
        return self.title   


    class Meta:
        ordering = ('title',)

    # def get_absolute_url(self):
    #     return reverse('/movies', kwargs={'id': self.id})

# class User(User):
#     # username   = models.CharField(max_length=200, primary_key=True, blank=False)
#     ratings    = models.ManyToManyField(Movie, through='RatingMovie')

#     def __str__(self):
#         return self.username


class RatingMovie(models.Model):
    movie      = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    #personalized rating
    p_rating   = models.IntegerField( validators=[MinValueValidator(0), MaxValueValidator(5)],
                                        default=0)
                                        
    def __str__(self):
        return (self.movie.title + ', ' + self.user.username + ', ' + str(self.p_rating) ) 

    # def get_absolute_url(self):
    #     return reverse("/rate_movie", kwargs={"id": self.id})

class Party(models.Model):
    n_members = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                    default=0)
    party_memberships = models.ManyToManyField(User)

    def __str__(self):
        return ('party id:' + str(self.id))
    
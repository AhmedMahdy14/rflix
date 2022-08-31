from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.urls import reverse


class Movie(models.Model):
    title = models.CharField(max_length=150)
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2200)],
                                   default=timezone.datetime.now().year)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    nratings = models.PositiveIntegerField(default=0)
    rated_by = models.ManyToManyField(User, through='RatingMovie')

    def __str__(self):
        return self.title   

    class Meta:
        ordering = ('title',)
        

class RatingMovie(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    p_rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
                                        
    def __str__(self):
        return self.movie.title + ', ' + self.user.username + ', ' + str(self.p_rating)


class Party(models.Model):
    n_members = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                    default=0)
    name = models.CharField(max_length=150, null=True, blank=True)
    party_memberships = models.ManyToManyField(User)

    def __str__(self):
        return 'party id:' + str(self.id)

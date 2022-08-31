from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.contrib.auth.models import User
from .models import RatingMovie


class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(label='User name')
    email = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect passsword")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class PersonalizedRating(forms.ModelForm):
    class Meta:
        model = RatingMovie
        fields = ('p_rating',)

    def clean(self, *args, **kwargs):
        p_rating = self.cleaned_data.get("p_rating")
        if not p_rating >= 1 and p_rating <= 5:
            return super(PersonalizedRating, self).clean(*args, **kwargs)
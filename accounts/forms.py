from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from .models import Profile
# from django.contrib.auth import get_user_model

# User = get_user_model()
# Lets do some manual login


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


    def clean_username(self):
        username = self.cleaned_data.get('username')
        # check if user exist with the username
        qs = User.objects.filter(username__iexact=username).count()

        if qs > 1:
            raise forms.ValidationError('Invalid Username')

        return username

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username).count()
        if qs:
            raise forms.ValidationError('Invalid Username')
        return username

    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Password mismatch')
        else:
            return password2


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'dob']
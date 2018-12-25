from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm



class SignupForm(forms.Form):
    username = forms.CharField(
    max_length=30,
    widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        max_length=2000,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm = forms.CharField(
        max_length=2000,
        widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter Password'}))

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already taken.")

        return cleaned_data



class LoginForm(forms.Form):
    username = forms.CharField(
    max_length=30,
    widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        max_length=2000,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self):
    # Confirms that the username exists in model database
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username__exact=username):
            print('no user')
            raise forms.ValidationError("User does not exist.")
        return cleaned_data

class changePassword(forms.Form):
    oldPwd = forms.CharField(label='oldPwd',max_length=100,widget = forms.PasswordInput())
    newPwd1 = forms.CharField(label='newPwd1',max_length=100,widget = forms.PasswordInput())
    newPwd2 = forms.CharField(label='newPwd2',max_length=100,widget = forms.PasswordInput())

    def clean(self):
        cleaned_data = super(changePassword, self).clean()
        newPwd1 = cleaned_data.get('newPwd1')
        newPwd2 = cleaned_data.get('newPwd2')

        if newPwd1 and newPwd2 and newPwd1 != newPwd2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

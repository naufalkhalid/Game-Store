from django import forms
from django.contrib.auth.models import User
from game_store.models import UserProfile
from django.contrib.auth import authenticate, login

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)

	class Meta:
		model = User
		fields = ('username', 'email', 'password','first_name','last_name')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('is_developer',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if (not user):
            raise forms.ValidationError("Incorrect Username or Password")
        elif (not user.is_active):
            raise forms.ValidationError("User is inactive")
        return self.cleaned_data
    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)

from django import forms
from django.contrib.auth.models import User
from game_store.models import UserProfile, Game
from django.contrib.auth import authenticate, login

class GameForm(forms.ModelForm):
	title = forms.CharField(max_length=250)
	href = forms.CharField(max_length=1000)
	category = forms.CharField(max_length=250)
	price=forms.DecimalField(max_digits=10, decimal_places=2)
	class Meta:
		model = Game
		fields = ('title', 'href', 'price','category',)

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	confirmPassword=forms.CharField(widget=forms.PasswordInput())
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	username = forms.CharField(max_length=100)
	email = forms.EmailField()
	def clean(self):
		password=self.cleaned_data.get('password')
		confirmPassword=self.cleaned_data.get('confirmPassword')
		if(password!=confirmPassword):
			msg="Password Donot Match"
			self.add_error("password",msg)
			self.add_error("confirmPassword",msg)
	class Meta:
		model = User
		fields = ('username', 'email', 'password','first_name','last_name')

class UserProfileForm(forms.ModelForm):
	is_developer = forms.BooleanField()
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


class PurchaseForm(forms.Form):
    pid = forms.CharField(widget=forms.HiddenInput())
    sid = forms.CharField(widget=forms.HiddenInput())
    success_url = forms.CharField(widget=forms.HiddenInput())
    cancel_url = forms.CharField(widget=forms.HiddenInput())
    error_url = forms.CharField(widget=forms.HiddenInput())
    checksum = forms.CharField(widget=forms.HiddenInput())
    def __init__(self, *args,**kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        #self.fields['pid'].initial = 

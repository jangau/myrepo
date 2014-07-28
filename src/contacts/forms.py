from django import forms
from models import MyUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 
class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ( "username", "email" )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('name', 'description')
from django import forms
from.models import postspage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class postform(forms.ModelForm):
    class Meta:
        model=postspage
        fields=['category','image','content',]
        lables={
            'category':'Category',
            'content':'Leave any specific content',
        }

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
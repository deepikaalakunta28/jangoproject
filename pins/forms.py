from django import forms
from boards.models import Board
from .models import Pin
from profileApp.models import Profile


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'description', 'is_private']

class PinForm(forms.ModelForm):
    class Meta:
        model = Pin
        fields = ['title', 'description', 'image', 'board']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["photo", "bio", "website", "location"]

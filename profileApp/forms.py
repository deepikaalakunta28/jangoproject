from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            "class": "profile-photo-input",
            "accept": "image/*",
        })
    )
    class Meta:
        model = Profile
        fields = ["photo", "bio", "website", "location"]

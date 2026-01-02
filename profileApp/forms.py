from django import forms
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_image", "bio", "website", "location"]

        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
            "website": forms.URLInput(attrs={"placeholder": "https://"}),
            "location": forms.TextInput(attrs={"placeholder": "City, Country"}),
        }

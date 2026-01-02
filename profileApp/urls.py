from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_profile, name="my_profile"),   # /profile/
    
    # EDIT PROFILE must come before <username>
    path("edit/", views.edit_profile, name="edit_profile"),
    
    # USER PROFILE PAGE
    path("<str:username>/", views.profile_view, name="profile"),
]

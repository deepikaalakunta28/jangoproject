from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_profile, name="my_profile"),   # /profile/
    path("edit/", views.edit_profile, name="edit_profile"),
    path("<str:username>/", views.profile_view, name="profile"),
]

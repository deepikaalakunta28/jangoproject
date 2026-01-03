from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm

from boards.models import Board
from pins.models import Pin

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.userprofile

    tab = request.GET.get("tab", "boards")   # default tab = boards

    boards = Board.objects.filter(user=user)
    pins = Pin.objects.filter(user=user)
    saved_pins = user.saved_pins.all()

    return render(request, "profileApp/profile.html", {
        "profile_user": user,
        "profile": profile,
        "boards": boards,
        "pins": pins,
        "saved_pins": saved_pins,
        "tab": tab,
    })



@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profileApp/edit_profile.html", {
        "form": form
    })


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def my_profile(request):
    return redirect("profile", username=request.user.username)

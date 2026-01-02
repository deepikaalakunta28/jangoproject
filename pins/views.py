from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BoardForm, PinForm
from boards.models import Board
from .models import Pin, Comment, Like
from django.http import JsonResponse

from django.shortcuts import render
from .models import Pin

def home(request):
    pins = Pin.objects.all()
    return render(request, "home.html", {"pins": pins})



# @login_required
# def home(request):
#     pins = Pin.objects.filter(user=request.user)  
#     return render(request, 'home.html', {'pins': pins})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()  

        if not username or not email or not password:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('register')

        if confirm_password and password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('login')

    return render(request, 'register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required
def create_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.user = request.user  
            board.save()
            return redirect('boards_list')
    else:
        form = BoardForm()
    return render(request, 'boards/create_board.html', {'form': form})


@login_required
def create_pin(request):
    boards = Board.objects.filter(user=request.user) 
    if not boards.exists():
        messages.error(request, "You need to create a board first!")
        return redirect('boards_list')

    # if not boards.exists():
    #     messages.error(request, "You need to create a board first!")
    #     return redirect('create_board')

    if request.method == 'POST':
        form = PinForm(request.POST, request.FILES)
        form.fields['board'].queryset = boards
        if form.is_valid():
            pin = form.save(commit=False)
            pin.user = request.user
            pin.save()
            return redirect('home')
    else:
        form = PinForm()
        form.fields['board'].queryset = boards

    return render(request, 'pins/create_pin.html', {'form': form})


# def board_list(request):
#     boards = Board.objects.all()
#     return render(request, 'boards/board_list.html', {'boards': boards})
def board_list(request):
    return redirect('boards_list')


@login_required
def pin_list(request):
    pins = Pin.objects.filter(user=request.user)
    return render(request, 'pins/pin_list.html', {'pins': pins})

def delete_pin(request, pk):
    pin = get_object_or_404(Pin, pk=pk)
    if request.user == pin.owner:
        pin.delete()
    return redirect('home')

from django.shortcuts import render, get_object_or_404
from boards.models import Board
from .models import Pin

def pin_detail(request, pin_id):
    pin = get_object_or_404(Pin, id=pin_id)

    user_boards = Board.objects.filter(user=request.user)

    other_pins = Pin.objects.filter(
        board=pin.board
    ).exclude(id=pin.id)[:6]

    # 👇 ADD THIS
    user_liked = pin.likes.filter(user=request.user).exists()

    return render(request, "pins/pin_detail.html", {
        "pin": pin,
        "other_pins": other_pins,
        "user_boards": user_boards,
        "user_liked": user_liked,   # 👈 pass flag
    })


@login_required
def add_comment(request, pin_id):
    pin = get_object_or_404(Pin, id=pin_id)

    if request.method == "POST":
        text = request.POST.get("comment")
        if text:
            Comment.objects.create(
                pin=pin,
                user=request.user,
                text=text
            )
    return redirect('pin_detail', pin_id=pin_id)


from django.http import JsonResponse
from .models import Like

@login_required
def toggle_like(request, pin_id):
    pin = get_object_or_404(Pin, id=pin_id)
    user = request.user

    like, created = Like.objects.get_or_create(pin=pin, user=user)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes_count": pin.likes.count()
    })



from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Pin

@login_required
def save_pin(request, pin_id):
    pin = get_object_or_404(Pin, id=pin_id)

    if request.user in pin.saved_by.all():
        pin.saved_by.remove(request.user)
        saved = False
    else:
        pin.saved_by.add(request.user)
        saved = True

    return JsonResponse({"saved": saved})


def profile_view(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    saved_pins = profile.user.saved_pins.all()  
    context = {
        'profile': profile,
        'saved_pins': saved_pins,
    }
    return render(request, 'profile.html', context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def delete_pin(request, pin_id):
    pin = get_object_or_404(Pin, id=pin_id, user=request.user)

    if request.method == "POST":
        pin.delete()
        return redirect("home")

    return render(request, "pins/confirm_delete_pin.html", {"pin": pin})


from .models import Pin
from boards.models import Board

from django.contrib.auth.decorators import login_required
from .forms import PinForm
from .models import Board

 

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from boards.models import Board
from .forms import PinForm


@login_required
def create_pin(request, board_id=None):
    board = None

    # If board_id is provided (coming from "Add Pin" button on a board)
    if board_id:
        board = get_object_or_404(Board, id=board_id, user=request.user)

    if request.method == "POST":
        form = PinForm(request.POST, request.FILES)

        if form.is_valid():
            pin = form.save(commit=False)
            pin.user = request.user

            # Force-assign to board if opened from board page
            if board:
                pin.board = board

            pin.save()
            return redirect("board_detail", board.id if board else pin.board.id)

    else:
        form = PinForm()

        # Pre-select the board in dropdown
        if board:
            form.fields["board"].initial = board.id

    return render(
        request,
        "pins/create_pin.html",
        {"form": form, "board": board},
    )


from django.db.models import Q
from .models import Pin

def search_pins(request):
    query = request.GET.get("q", "")

    pins = Pin.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query)
    )

    return render(request, "pins/search_results.html", {
        "query": query,
        "pins": pins
    })


from boards.models import Board
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

@login_required
def move_pin(request, pin_id):
    pin = get_object_or_404(Pin, id=pin_id, user=request.user)

    if request.method == "POST":
        new_board_id = request.POST.get("board_id")
        new_board = get_object_or_404(Board, id=new_board_id, user=request.user)

        pin.board = new_board
        pin.save()

        messages.success(request, "Pin moved successfully!")
        return redirect("pin_detail", pin_id=pin.id)

    return redirect("pin_detail", pin_id=pin.id)

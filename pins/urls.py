from django.urls import path
from django.shortcuts import redirect
from . import views

def redirect_to_home(request):
    return redirect('home')

urlpatterns = [
    path('', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('boards/create/', views.create_board, name='create_board'),
    # path('boards/', views.board_list, name='board_list'),
    path('pins/create/', views.create_pin, name='create_pin'),
    path('delete/<int:pk>/', views.delete_pin, name='delete_pin'),
    path('pin/<int:pin_id>/', views.pin_detail, name='pin_detail'),
    path('pin/<int:pin_id>/add_comment/', views.add_comment, name='add_comment'),
    path('toggle-like/<int:pin_id>/', views.toggle_like, name='toggle_like'),
    path('save/<int:pin_id>/', views.save_pin, name='save_pin'),
    path("pin/<int:pin_id>/delete/", views.delete_pin, name="delete_pin"),
    path("create/<int:board_id>/", views.create_pin, name="create_pin"),
    path("search/", views.search_pins, name="search_pins"),
    path("create/", views.create_pin, name="create_pin"),
    path("create/<int:board_id>/", views.create_pin, name="create_pin_board"),
    path("pin/<int:pin_id>/move/", views.move_pin, name="move_pin"),

]
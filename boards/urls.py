from django.urls import path
from . import views

urlpatterns = [
    path('', views.boards_list, name='boards_list'),
    path('create/', views.create_board, name='create_board'),
    path('detail/<int:board_id>/', views.board_detail, name='board_detail'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path("delete/<int:board_id>/", views.delete_board, name="delete_board"),
    path("delete/<int:board_id>/", views.delete_board, name="delete_board"),
    path("<int:board_id>/", views.board_detail, name="board_detail"),

]

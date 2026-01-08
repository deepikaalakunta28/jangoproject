from django.urls import path
from . import views

urlpatterns = [
    path("", views.register, name="register"),
    path("home/", views.home, name="home"),

    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("pins/create/<int:board_id>/", views.create_pin, name="create_pin"),
    path("pins/create/", views.create_pin, name="create_pin"),

    path("create/<int:board_id>/", views.create_pin, name="create_pin_for_board"),

    path("pin/<int:pin_id>/", views.pin_detail, name="pin_detail"),
    path("pin/<int:pin_id>/move/", views.move_pin, name="move_pin"),
    path("pin/<int:pin_id>/delete/", views.delete_pin, name="delete_pin"),
    path("pin/<int:pin_id>/add_comment/", views.add_comment, name="add_comment"),
    path("pin/<int:pin_id>/like/", views.toggle_like, name="toggle_like"),

    path("save/<int:pin_id>/", views.save_pin, name="save_pin"),

    path("search/", views.search_pins, name="search_pins"),

    # Profile
    # --- Profile ---

    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.profile_view, name="profile"),
    path("profile/<str:username>/follow/", views.toggle_follow, name="toggle_follow"),

]

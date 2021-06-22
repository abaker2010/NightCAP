from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

app_name = "accounts"
urlpatterns = [
    path(
        "profile/",
        views.ProfileView.as_view(template_name="accounts/profile.html"),
        name="profile",
    ),
    path(
        "",
        views.ProfileView.as_view(template_name="accounts/profile.html"),
    ),
    # Django Auth Stuff
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="public/index"),
        name="logout",
    ),
]

from django.urls import path

from .views import (
    login,
    signup,
    logout,
    profile,
    contact,
    verify_code,
    edit_profile,
    generate_code,
    change_password,
)

urlpatterns = [
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", logout, name="loggetout"),
    path("profile/", profile, name="profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("contact/", contact, name="contact"),
    path("verify/", verify_code, name="verify_code"),
    path("generate/", generate_code),
    path("change/password/", change_password),
]

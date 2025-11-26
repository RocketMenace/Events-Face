from django.urls import path

from .apps import AuthenticationConfig
from .views import LoginAPI, LogoutAPI, RefreshAPI, UserCreateAPI

app_name = AuthenticationConfig.name


urlpatterns = [
    path("register", UserCreateAPI.as_view(), name="register"),
    path("login", LoginAPI.as_view(), name="login"),
    path("logout", LogoutAPI.as_view(), name="logout"),
    path("refresh", RefreshAPI.as_view(), name="refresh-token"),
]

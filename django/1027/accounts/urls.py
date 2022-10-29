from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("update/", views.update, name="update"),
    path("<int:user_pk>/", views.detail, name="detail"),
    path("<int:user_pk>/follow/", views.follow, name="follow"),
    path("password/", views.changePassword, name="changePassword"),
    path("delete/", views.delete, name="delete"),
]

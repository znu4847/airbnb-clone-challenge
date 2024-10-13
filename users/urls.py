from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("password", views.Password.as_view()),
    path("password/<int:pk>", views.PasswordManager.as_view()),
    path("login", views.LogIn.as_view()),
    path("logout", views.LogOut.as_view()),
    path("<int:pk>", views.Public.as_view()),
    path("<int:pk>/tweets", views.Tweets.as_view()),
]

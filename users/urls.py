from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>/tweets", views.Users.as_view()),
]

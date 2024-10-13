from django.urls import path
from . import views

urlpatterns = [
    path("", views.Tweets.as_view()),
    path("<int:pk>", views.Detail.as_view()),
]

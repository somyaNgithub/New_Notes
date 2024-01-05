from . import views
from django.urls import path

urlpatterns = [
    path('auth/signup', views.signup, name = "signup"),
    path('auth/login', views.login, name = "login"),
]
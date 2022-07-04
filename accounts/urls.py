
from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name="accounts/login.html"), name='login'),
]
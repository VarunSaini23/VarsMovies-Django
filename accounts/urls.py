from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.auth_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]

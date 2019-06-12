from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from movies import views as movie_views

urlpatterns = [
    path('search/<slug:query>', movie_views.search, name="search"),
    path('detail/<int:movie_id>', movie_views.detail, name="movie_detail"),
    path('detail/<int:movie_id>/addToCollection', movie_views.add_to_collection, name="add_to_collection"),

]

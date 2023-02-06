"""hollymovies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import api.views
from django.contrib import admin
from django.urls import path, include

from viewer.views import *
from accounts.views import SignUpView

from api.views import *

from rest_framework import *

urlpatterns = [
    # app viewer
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('hello/<s>/', hello, name='hello'),
    path('hello2/', hello2, name='hello2'),
    path('movies/', MoviesView.as_view(), name='movies'),
    path('movies/filter_movies/', filter_movies, name='filter_movies'),
    path('movie/<pk>/', movie, name='movie'),
    path('new_movie/', MovieCreateView.as_view(), name='new_movie'),
    #path('new_movie/add_movie/', add_movie, name='add_movie'),
    path('movie/update/<pk>/', MovieUpdateView.as_view(), name='update_movie'),
    path('movie/delete/<pk>/', MovieDeleteView.as_view(), name='delete_movie'),
    path('top_movies/', movie_by_rating, name='movies_by_rating'),
    path('last_visited_movies/', last_visited_movies, name='last_visited_movies'),
    path('new_movies/', new_movies, name='new_movies'),
    path('random_movie/', random_movie, name='random_movie'),
    path('staff/<pk>/', staff, name='staff'),
    path('actors/', actors, name='actors'),
    path('search/', search, name='search'),
    path('rate_movie/', rate_movie, name='rate_movie'),

    # app accounts
    #path('accounts/', include('accounts.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),    # signup
    path('accounts/', include('django.contrib.auth.urls')),  # login, logout, password_change,...

    # api
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('api/movies/', api.views.Movies.as_view({'get': 'list'})),
    path('api/movies/', api.views.Movies.as_view()),
    path('api/movie/<pk>/', api.views.Movie.as_view()),
]

from django.shortcuts import render
from django.http import HttpResponse
from viewer.models import *

# Create your views here.
def home(request):
    return render(request, 'home.html')

def hello(request, s):
    adjectives = ['wunderfull', 'nice', 'blue', s]
    context = {'adjectives': adjectives, 'name': 'Petr'}
    return render(request, 'hello.html', context)
    #return HttpResponse(f"Hello, {s} world!")

def hello2(request):
    s = request.GET.get('s', '')
    return HttpResponse(f"Hello, {s} world!")

def movies(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movies.html', context)

def movie(request, pk):
    movie = Movie.objects.get(id=pk)
    countries = Country.objects.filter(movies=movie)
    genres = Genre.objects.filter(movies=movie)
    images = Image.objects.filter(movies=movie)
    directors = Staff.objects.filter(directing=movie)
    actors = Staff.objects.filter(acting=movie)
    context = {'movie': movie, 'countries': countries,
               'genres': genres, 'images': images,
               'directors': directors, 'actors': actors}
    return render(request, 'movie.html', context)
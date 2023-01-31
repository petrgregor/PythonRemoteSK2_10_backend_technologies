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
    context = {'movie': movie}
    return render(request, 'movie.html', context)
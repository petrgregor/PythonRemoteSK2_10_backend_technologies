from django.shortcuts import render, redirect
from django.http import HttpResponse
from viewer.models import *
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, \
    CreateView, UpdateView, DeleteView
from django.forms import *
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import random

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

"""
# již nepoužíváme, nahradili jsme pomocí MoviesView
def movies(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movies.html', context)
"""

"""
# version 1: with method
class MoviesView(View):
    def get(self, request):
        movies = Movie.objects.all()
        context = {'movies': movies}
        return render(request, 'movies.html', context)
"""

"""
# version 2: TemplateView
class MoviesView(TemplateView):
    template_name = 'movies.html'
    movies = Movie.objects.all()
    extra_context = {'movies': movies}
"""

# version 3: ListView
class MoviesView(ListView):
    template_name = 'movies.html'
    model = Movie


def filter_movies(request):
    # TODO: filtrovat i nehodnocené filmy (podle žánru)
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    genre_name = ""
    context = {'genres': genres}
    min_rating = 1
    filtered_movies = []
    if request.method == 'POST':
        genre_name = request.POST.get('genre').strip()
        if Genre.objects.filter(name=genre_name).count() > 0:
            genre = Genre.objects.get(name=genre_name)
            genre_name = genre.name
            movies = Movie.objects.filter(genre=genre)
        if request.POST.get('rating'):
            min_rating = float(request.POST.get('rating'))
            for movie in movies:
                if Rating.objects.filter(movie=movie).count() > 0:
                    if float(Rating.objects.filter(movie=movie).aggregate(Avg('rating'))['rating__avg']) >= min_rating:
                        filtered_movies.append(movie)
        else:
            filtered_movies = movies
        context = {'object_list': filtered_movies, 'genres': genres, 'selected_genre': genre_name,
                   'min_rating': min_rating}

    return render(request, 'filter_movies.html', context)


def capitalized_validator(value):
  if value[0].islower():
    raise ValidationError('Value must be capitalized.')

"""
@permission_required
def new_movie(request):
    return render(request, 'new_movie.html')
"""

"""
def add_movie(request):
    #capitalized_validator(request.POST.get('title_orig'))
    Movie.objects.create(
        title_orig=request.POST.get('title_orig'),
        title_cz=request.POST.get('title_cz'),
        title_sk=request.POST.get('title_sk'),
        released=request.POST.get('released')
    )
    return render(request, 'movies.html')
"""

"""
# Formulář pomocí třídy Form
class MovieForm(Form):
    title_orig = CharField(max_length=64)
    title_cz = CharField(max_length=64)
    title_sk = CharField(max_length=64)
    genre = ModelChoiceField(queryset=Genre.objects)
    released = IntegerField()
    description = CharField(widget=Textarea, required=False)

    def clean_title_orig(self):
        initial = super().clean()
        initial = initial['title_orig']
        #initial = self.cleaned_data['title_orig']
        print(f"initial: {initial}, capitalize: {initial.capitalize()}")
        return initial.capitalize()

    def clean(self):
        result = super().clean()
        return result
"""

class MovieForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Movie
        #fields = '__all__'
        exclude = ['last_visit']

    def clean_title_orig(self):
        cleaned_data = super().clean()
        title_orig = cleaned_data.get('title_orig')
        #if title_orig == None:
        #    raise ValidationError("Title can not be empty.")
        return title_orig

    def clean_released(self):
        cleaned_data = super().clean()
        released = cleaned_data.get('released')
        #if released < 1900 or released > 2023:
        #    raise ValidationError("Invalid year")
        return released

    def clean(self):
        cleaned_data = self.cleaned_data
        print(cleaned_data)
        return cleaned_data

    released = IntegerField(min_value=1900, max_value=datetime.now().year)

"""
# with FormView
class MovieCreateView(FormView):
  template_name = 'new_movie.html'
  form_class = MovieForm
"""

class MovieCreateView(PermissionRequiredMixin, CreateView):
  template_name = 'new_movie.html'
  form_class = MovieForm
  success_url = reverse_lazy('home')
  permission_required = 'viewer.add_movie'


class MovieUpdateView(PermissionRequiredMixin, UpdateView):
  template_name = 'new_movie.html'
  model = Movie
  form_class = MovieForm
  success_url = reverse_lazy('home')
  permission_required = 'viewer.change_movie'


class MovieDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'movie_confirm_delete.html'
    model = Movie
    success_url = reverse_lazy('home')
    permission_required = 'viewer.delete_movie'


def movie(request, pk):
    try:
        movie = Movie.objects.get(id=pk)
        movie.last_visit = datetime.now()
        movie.save()
        countries = Country.objects.filter(movies=movie)
        genres = Genre.objects.filter(movies=movie)
        images = Image.objects.filter(movies=movie)
        directors = Staff.objects.filter(directing=movie)
        actors = Staff.objects.filter(acting=movie)

        # rating
        avg_rating = None
        if Rating.objects.filter(movie=movie).count() > 0:
            avg_rating = Rating.objects.filter(movie=movie).aggregate(Avg('rating'))
        # users rating
        user = request.user
        user_rating = None
        if request.user.is_authenticated:
            if Rating.objects.filter(movie=movie, user=user).count() > 0:
                user_rating = Rating.objects.get(movie=movie, user=user)

        comments = Comment.objects.filter(movie=movie)

        context = {'movie': movie, 'countries': countries,
                   'genres': genres, 'images': images,
                   'directors': directors, 'actors': actors,
                   'avg_rating': avg_rating, 'user_rating': user_rating,
                   'comments': comments}
        return render(request, 'movie.html', context)
    except:
        return render(request, 'home.html', {'error_message': 'Movie not found'})

def staff(request, pk):
    staff = Staff.objects.get(id=pk)
    awards = Award.objects.filter(staff=staff)
    directing_movies = Movie.objects.filter(directing_movie=staff)
    acting_in_movies = Movie.objects.filter(acting_in_movie=staff)
    context = {'staff': staff, 'awards': awards,
               'directing_movies': directing_movies,
               'acting_in_movies': acting_in_movies}
    return render(request, 'staff.html', context)

def actors(request):
    staff_set = Staff.objects.all()
    actors = []
    for staff in staff_set:
        if Movie.objects.filter(acting_in_movie=staff).count() > 0:
            actors.append(staff)
    context = {'actors': actors}
    return render(request, 'actors.html', context)

def search(request):
    if request.method == 'POST':  # pokud jsme poslali dotaz z formuláře
        search = request.POST.get('search')
        search = search.strip()
        if len(search) > 0:
            movies_title_orig = Movie.objects.filter(title_orig__contains=search)
            movies_title_cz = Movie.objects.filter(title_cz__contains=search)
            movies_title_sk = Movie.objects.filter(title_sk__contains=search)
            movies_descr = Movie.objects.filter(description__contains=search)
            staff_names = Staff.objects.filter(name__contains=search)
            staff_surnames = Staff.objects.filter(surname__contains=search)

            context = {'search': search, 'movies_title_orig': movies_title_orig,
                       'movies_title_cz': movies_title_cz, 'movies_title_sk': movies_title_sk,
                       'movies_descr': movies_descr,
                       'staff_names': staff_names, 'staff_surnames': staff_surnames}
            return render(request, 'search.html', context)
    return render(request, 'home.html')

def rate_movie(request):
    user = request.user
    if request.method == 'POST':
        pk = request.POST.get('movie_id')
        movie = Movie.objects.get(id=pk)
        rating = request.POST.get('rating')

        if Rating.objects.filter(movie=movie, user=user).count() > 0:
            user_rating = Rating.objects.get(movie=movie, user=user)
            user_rating.rating = rating
            user_rating.save()
        else:
            Rating.objects.create(
                movie=movie,
                user=user,
                rating=rating
            )
    return redirect(f"/movie/{pk}/")

def movie_by_rating(request):
    movies = Movie.objects.annotate(avg_rating=Avg('movie_rating__rating')).filter(avg_rating__gte=1.0).order_by('-avg_rating')[:10]
    context = {'movies': movies}
    return render(request, 'movies_by_rating.html', context)

def last_visited_movies(request):
    movies = Movie.objects.all().order_by('-last_visit')[:10]
    context = {'movies': movies}
    return render(request, 'last_visited_movies.html', context)

def new_movies(request):
    movies = Movie.objects.all().order_by('-created')[:10]
    context = {'movies': movies}
    return render(request, 'new_movies.html', context)

def random_movie(request):
    movies = Movie.objects.all()
    movie = random.choice(movies)
    context = {'movie': movie}
    return render(request, 'movie.html', context)


# Josef Krčmář
class StaffForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Staff
        fields = '__all__'

    #released = IntegerField(min_value=1900, max_value=datetime.now().year)


# Josef Krčmář
class StaffCreateView(PermissionRequiredMixin, CreateView):
  template_name = 'new_staff.html'
  form_class = StaffForm
  success_url = reverse_lazy('home')
  permission_required = 'viewer.add_staff'


# Josef Krčmář
class StaffUpdateView(PermissionRequiredMixin, UpdateView):
  template_name = 'new_staff.html'
  model = Staff
  form_class = StaffForm
  success_url = reverse_lazy('home')
  permission_required = 'viewer.change_staff'


# Josef Krčmář
class StaffDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'staff_confirm_delete.html'
    model = Staff
    success_url = reverse_lazy('home')
    permission_required = 'viewer.delete_staff '

def add_comment(request):
    if request.method == 'POST':
        pk = request.POST.get('movie_id')
        comment = request.POST.get('comment').strip()
        if len(comment) > 0:
            Comment.objects.create(
                movie=Movie.objects.get(id=pk),
                user=request.user,
                comment=comment
            )
    return redirect(f"/movie/{pk}/")

def edit_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.user == comment.user:
        if request.method == 'POST':
            comment_body = request.POST.get('comment').strip()
            comment.comment = comment_body
            comment.save()
            return redirect(f"/movie/{comment.movie.id}/")

        # else - tj. pokud ještě neposíláme data z formuláře
        context = {'comment': comment}
        return render(request, 'edit_comment.html', context)
    return redirect(f"/movie/{comment.movie.id}/")

def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.user == comment.user:
        if request.method == 'POST':
            comment.delete()
            return redirect(f"/movie/{comment.movie.id}/")

        # else
        context = {'comment': comment}
        return render(request, 'comment_confirm_delete.html', context)
    return redirect(f"/movie/{comment.movie.id}/")

def users_activity(request):
    user_ratings = User.objects.\
        annotate(num_rating=Count('user_rating__rating'), avg_rating=Avg('user_rating__rating')).order_by('-num_rating')[:10]
    user_comments = User.objects.annotate(num_comment=Count('user_comment__comment')).order_by('-num_comment')[:10]
    context = {'user_ratings': user_ratings, 'user_comments': user_comments}
    return render(request, 'users_activity.html', context)


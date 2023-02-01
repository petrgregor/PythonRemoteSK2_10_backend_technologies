from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, get_user_model
from django.views import generic
from django.urls import reverse_lazy

# Create your views here.

# our signup form
class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        #fields = '__all__'  # vybere všechny položky (sloupce)
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2') # nebo jen vypíšeme výběr


# our signup view
class SignUpView(generic.CreateView):
    # připojíme vytvořený formulář
    form_class = SignUpForm
    success_url = reverse_lazy('home')  # kam nás to přesměruje v případě úspěchu
    template_name = 'signup.html'  # použije se tento template

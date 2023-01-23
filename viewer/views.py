from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hello(request, s):
    return HttpResponse(f"Hello, {s} world!")

def hello2(request):
    s = request.GET.get('s', '')
    return HttpResponse(f"Hello, {s} world!")
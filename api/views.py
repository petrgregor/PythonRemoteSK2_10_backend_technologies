from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework import mixins

from viewer.models import Movie

from api.serializers import MovieSerializer

# Create your views here.
class Movies(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]
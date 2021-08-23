from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    return render(request, 'index.html')

def upload_images(request):
    if request.method == 'GET':
        return render(request, 'uploadImage.html')
    else:
         
        return render(request, 'uploadImage.html')

def login(request):
    return render(request, 'login.html')
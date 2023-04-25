from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse

def main(request):
    return render(request,"main.html")

def about(request):
    return render(request,"about.html")

def reviews(request):
    return render(request,"reviews.html")
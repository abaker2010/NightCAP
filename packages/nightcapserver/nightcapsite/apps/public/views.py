from django.shortcuts import render
from django.http.request import HttpRequest

def index(request: HttpRequest) -> HttpRequest:
    return render(request, 'index.html')

def about(request: HttpRequest) -> HttpRequest:
    return render(request, 'about.html')

def contact(request: HttpRequest) -> HttpRequest:
    return render(request, 'contact.html')

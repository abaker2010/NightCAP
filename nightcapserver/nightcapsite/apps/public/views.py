from django.shortcuts import render
from django.http.request import HttpRequest


def index(request: HttpRequest) -> HttpRequest:
    return render(request, "public/index.html")


def about(request: HttpRequest) -> HttpRequest:
    return render(request, "public/about.html")


def contact(request: HttpRequest) -> HttpRequest:
    return render(request, "public/contact.html")

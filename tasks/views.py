from django.http import HttpResponse


def home(request):
    return HttpResponse("Привет! Всё работает!")


from django.shortcuts import render

# Create your views here.

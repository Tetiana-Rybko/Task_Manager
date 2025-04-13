from django.http import HttpResponse

def home(request):
    return HttpResponse("Привет! Всё работает!")


# Create your views here.

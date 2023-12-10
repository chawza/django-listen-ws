from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def counter(requust):
    return render(requust, 'counter.html')


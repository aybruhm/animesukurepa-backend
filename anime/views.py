from django.shortcuts import render


def home(request):
    return render(request, 'base.html')

def search(request):
    return render(request, 'anime/index.html')
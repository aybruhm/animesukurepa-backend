from django.shortcuts import render
from .models import Search


def home(request):
    return render(request, 'base.html')

def search(request):
    search = request.POST.get('title')
    print(search)
    context = {'search': search}
    return render(request, 'anime/index.html', context)
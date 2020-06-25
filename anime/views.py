from django.shortcuts import render
from . import models
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus



AnimeUrl = 'https://www19.gogoanime.io//search.html?keyword={}'

def home(request):
    return render(request, 'base.html')

def search(request):
    search = request.POST.get('title') # Gets whatever you search for
    models.Search.objects.create(search=search) # Saves whatever you search for into the database
    searchURL = AnimeUrl.format(quote_plus(search)) # Takes what you search for and inserts it in AnimeUrl(Original Url)
    response = requests.get(searchURL) # this gets the whole URL address (e.g https://www19.gogoanime.io//search.html?keyword=whatever+you+searched+for)
    data = response.text # prints the source code for debugging sake
    soup = BeautifulSoup(data, 'lxml')
    
    anime_listings = soup.find('ul', {'class':'items'})

    for anime in anime_listings:
        anime_title = anime.find('ul', {'class':'items'})
        anime_url = anime.find('p', {'class': 'name'})
        anime_images = anime.find('img').text

    
        anime_listings.append((anime_title, anime_url, anime_images))


    context = {'search': search, 'anime_listings': anime_listings}
    return render(request, 'anime/index.html', context)
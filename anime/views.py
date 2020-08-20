from django.shortcuts import render
from . import models
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus


AnimeUrl = 'https://www19.gogoanime.io//search.html?keyword={}'


def home(request):
    return render(request, 'base.html')


def search(request):
    # Gets whatever you search for
    search = request.POST.get('title')
    # Saves whatever you search for into the database
    models.Search.objects.create(search=search)
    # Takes what you search for and inserts it in AnimeUrl(Original Url)
    searchURL = AnimeUrl.format(quote_plus(search))
    # this gets the whole URL address (e.g https://www19.gogoanime.io//search.html?keyword=whatever+you+searched+for)
    response = requests.get(searchURL)
    # Extracting the source code of the page
    data = response.text
    # Passing the source code to Beautiful Soup to create an object for it
    soup = BeautifulSoup(data, 'lxml')
    # Extracting all the div's with the class 'last_episodes'
    anime_listings = soup.find('div', class_='last_episodes')

    # Creates an empty list to store scraped_animes
    scraped_animes = []

    for anime in anime_listings.find_all('li'):

        title = anime.find('p', class_='name').text
        img_src = anime.find('img').get('src')
        img_alt = anime.find('img').get('alt')
        a_link = anime.find('a').get('href')
        releases = anime.find('p', class_="released").text

        # Stores the scraped data into a list
        scraped_animes.append((title, img_src, img_alt, a_link, releases))

    context = {'search': search, 'scraped_animes': scraped_animes}
    return render(request, 'anime/index.html', context)

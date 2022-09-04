# Rest Framework Imports
from rest_framework import views,  status
from rest_framework.request import Request
from rest_framework.response import Response

# DRF Yasg Imports
from drf_yasg.utils import swagger_auto_schema

# Typing Imports
from typing import List

# Own Imports
from anime.models import Search
from anime.serializers import SearchSerializer

# Third Party Imports
from bs4 import BeautifulSoup
import httpx
from requests.compat import quote
from decouple import config
from rest_api_payload import success_response, error_response



anime_url = config("ANIME_URL")


class AnimeSearch(views.APIView):
    serializer_class = SearchSerializer
    
    def quote_search_keyword(self, keyword:str, safe="", encoding=None, errors=None):
        """Like quote(), but also replace ' ' with '+', as required for quoting
        HTML form values. Plus signs in the original string are escaped unless
        they are included in safe. It also does not have safe default to '/'.
        """
        # Check if ' ' in string, where string may either be a str or bytes.  If
        # there are no spaces, the regular quote will produce the right answer.
        if ((isinstance(keyword, str) and ' ' not in keyword) or
            (isinstance(keyword, bytes) and b' ' not in keyword)):
            return quote(keyword, safe, encoding, errors)
        if isinstance(safe, str):
            space = ' '
        else:
            space = b' '
            
        keyword = quote(keyword, safe + space, encoding, errors)
        return keyword.replace(' ', '-')
    
    
    def anime_scrape(self, keyword:str) -> List:
        
        # Saves whatever you search for into the database
        search_keyword, _ = Search.objects.get_or_create(name=keyword)
        
        # if search_keyword:
        #     ...
        
        # else:
        #     ...
        
        # Takes what you search for and inserts it in anime_url(Original Url)
        searchURL = anime_url.format(self.quote_search_keyword(keyword=keyword))
        response = httpx.get(searchURL)
        
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
            release = anime.find('p', class_="released").text 

            # Stores the scraped data into a list
            scraped_animes.append((title, img_src, img_alt, a_link, release))
            
            
        return scraped_animes, True
    
    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request:Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            
            # search through anime site or database
            try:
                results, isTrue = self.anime_scrape(keyword=name)
            except (Exception, ConnectionError) as e:
                payload = error_response(status=False, message=f"{e}")
                return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
            
            # success n
            if isTrue:
                payload = success_response(
                    status=True, message=f"{name} anime searched",
                    data={"animes": results}
                )
                return Response(data=payload, status=status.HTTP_200_OK)

            else:
                payload = error_response(status=False, message="Oof. No such anime was found. Try.. again?")
                return Response(data=payload, status=status.HTTP_404_NOT_FOUND)
        else:
            payload = error_response(status=False, message=serializer.errors)
            return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
        
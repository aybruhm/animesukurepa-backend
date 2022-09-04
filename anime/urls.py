from django.urls import path
from anime.views import AnimeSearch

app_name = "anime"

urlpatterns = [
    path("search/", AnimeSearch.as_view(), name="anime_search"),
]

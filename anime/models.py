from django.db import models


class Search(models.Model):
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Searched Anime"
        db_table = "searches"
        
    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Anime Categories"
        db_table = "anime_categories"
        
    def __str__(self) -> str:
        return self.name


class SavedAnime(models.Model):
    title = models.CharField(max_length=255)
    image_src = models.URLField()
    image_alt = models.CharField(max_length=255)
    anime_link = models.URLField()
    released = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Saved Animes"
        db_table = "saved_animes"
        
    def __str__(self) -> str:
        return self.title
    
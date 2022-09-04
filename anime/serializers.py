# Rest Framework Imports
from rest_framework import serializers

# Own Imports
from anime.models import Search


class SearchSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Search
        field = ["search"]
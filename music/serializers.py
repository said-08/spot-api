from rest_framework import serializers
from .models import *

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    artistId = ArtistSerializer()
    genreId = GenderSerializer()

    class Meta:
        model = Song
        fields = '__all__'

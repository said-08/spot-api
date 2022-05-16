from django.db import models
from django.db.models import ForeignKey
from django.db.models.fields import *

class Artist(models.Model):

    id = CharField(primary_key=True, max_length=255)
    name = CharField(max_length=255)
    url = CharField(max_length=255)

    class Meta:
        db_table = 'artist'
    
    def __str__(self):
        return self.artistName

class Gender(models.Model):

    id = CharField(primary_key=True, max_length=255)
    name = CharField(max_length=255)
    url = CharField(max_length=255)

    class Meta:
        db_table = 'gender'
    
    def __str__(self):
        return self.name

class Song(models.Model):

    id = CharField(primary_key=True, max_length=255)
    name = CharField(max_length=255)
    releaseDate = CharField(max_length=255)
    url = CharField(max_length=255)
    artistId = ForeignKey(Artist, on_delete=models.CASCADE)
    genreId = ForeignKey(Gender, on_delete=models.CASCADE)

    class Meta:
        db_table = 'song'

    def __str__(self):
        return self.name

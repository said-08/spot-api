from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
import requests
import json
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Song, Artist, Gender
from .serializers import ArtistSerializer, GenderSerializer, SongSerializer

@api_view(['GET'])
def init(request):
    try:
        req = requests.get('https://rss.applemarketingtools.com/api/v2/us/music/most-played/100/songs.json')
        data = json.loads(req.content)
        list = data['feed']['results']

        for element in list:
            try:
                artist = Artist.objects.create(
                    id = element['artistId'],
                    name = element['artistName'],
                    url = element['artistUrl']
                )
            except IntegrityError:
                pass
        
        for element in list:
            try:
                gender = Gender.objects.create(
                    id = element['genres'][0]['genreId'],
                    name = element['genres'][0]['name'],
                    url = element['genres'][0]['url']
                )
            except IntegrityError:
                pass
        
        for element in list:
            try:
                artist = Artist.objects.get(id=element['artistId'])
                gender = Gender.objects.get(id=element['genres'][0]['genreId'])
                song = Song.objects.create(
                    id = element['id'],
                    name = element['name'],
                    releaseDate = element['releaseDate'],
                    url = element['url'],
                    artistId = artist,
                    genreId = gender
                )
            except IntegrityError:
                pass

        return Response({
                'songs': SongSerializer(Song.objects.raw('SELECT * FROM song'), many=True).data
            })
    except Exception:
        return Response({'response': 'There was a problem :('})

@api_view(['GET'])
def songList(request):
    songs = SongSerializer(Song.objects.raw('SELECT * FROM song'), many=True)
    return Response(songs.data)

@api_view(['GET'])
def songByName(request, name):
    songs = SongSerializer(
        Song.objects.raw("SELECT * FROM song WHERE name = '{}'".format(name)),
        many=True
    )
    return Response(songs.data)

@api_view(['GET'])
def songTop50(request):
    songs = SongSerializer(Song.objects.raw('SELECT * FROM song LIMIT 50'), many=True)
    return Response(songs.data)

@api_view(['GET'])
def songsByGener(request):
    genders = GenderSerializer(Gender.objects.raw('SELECT * FROM gender'), many=True)
    response = {}
    for gender in genders.data:
        songs = SongSerializer(
            Song.objects.raw("SELECT * FROM song WHERE genreId_id = '{}'".format(gender['id'])),
            many=True
        )
        response[gender['name']] = songs.data
    return Response(response)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])   
@permission_classes([IsAuthenticated])
def createSong(request):
    try:
        artist = Artist.objects.get(id=request.data['artistId'])
        gender = Gender.objects.get(id=request.data['genreId'])
        song = Song.objects.create(
            id = request.data['id'],
            name = request.data['name'],
            releaseDate = request.data['releaseDate'],
            url = request.data['url'],
            artistId = artist,
            genreId = gender
        )
        return Response({'response': SongSerializer(song, many=False).data})
    except (Artist.DoesNotExist, Gender.DoesNotExist):
        return Response({'response': 'The artist or genre you are trying to enter does not exist'})
    except IntegrityError:
        return Response({'response': 'Invalid data'})
    except Exception:
        return Response({'response': 'There was a problem :('})
    

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteSong(request, id):
    try:
        song = Song.objects.get(id=id)
        song.delete()
        return Response({'response': 'Song deleted'})
    except Song.DoesNotExist:
        return Response({'response': "That song doesn't exist"})

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def createArtist(request):
    artist = ArtistSerializer(data=request.data)
    if artist.is_valid():
        artist.save()
        return Response(artist.data)
    else:
        return Response({'response': 'Invalid data'})

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteArtist(request, id):
    try:
        artist = Artist.objects.get(id=id)
        artist.delete()
        return Response({'response': 'Artist deleted'})
    except Artist.DoesNotExist:
        return Response({'response': "That artist doesn't exist."})

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def createGender(request):
    gender = GenderSerializer(data=request.data)
    if gender.is_valid():
        gender.save()
        return Response(gender.data)
    else:
        return Response({'response': 'Invalid data'})

@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteGender(request, id):
    try:
        gender = Gender.objects.get(genreId=id)
        gender.delete()
        return Response({'response': 'Gender deleted'})
    except Gender.DoesNotExist:
        return Response({'response': "That gender doesn't exist."})

@api_view(['POST'])
def login(request):
    username = request.data['username']
    password = request.data['password']
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'response': 'Nonexistent user'})
    pwd_valid = check_password(password, user.password)
    if not pwd_valid:
        return Response({'response': 'Invalid password'})
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})

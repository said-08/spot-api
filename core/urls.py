from django.contrib import admin
from django.urls import path, include
from music.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', init),
    path('songs/', songList),
    path('songs-name/<str:name>', songByName),
    path('songs-top-50/', songTop50),
    path('songs-gender/', songsByGener),
    path('create-song/', createSong),
    path('delete-song/<str:id>', deleteSong),
    path('create-artist/', createArtist),
    path('delete-artist/<str:id>', deleteArtist),
    path('create-gender/', createGender),
    path('delete-gender/<str:id>', deleteGender),
    path('login/', login)
]

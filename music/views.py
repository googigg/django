from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Album, Song
from django.http import Http404


from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AlbumSerializer

def hello(request,):
    return HttpResponse("Hello World!")

def index(request):
    # return HttpResponse("<h1>This is music App.</h1>" + html)

    allAlbums = Album.objects.all()
    # html = ''
    # for album in allAlbums:
    #     html += '<a href="/music/' + str(album.id) + '">' + album.artist + '</a>' + '</br>';

    # template = loader.get_template('music/index.html')
    context = {'allAlbums': allAlbums }


    # return HttpResponse(template.render(context, request))
    return render(request, 'index.html', context)

def detail(request, album_id):
    # return HttpResponse("<h2>Details for Album id: " + str(album_id) + "</h2>")
    #
    # try:
    #     album = Album.objects.get(pk=album_id)
    # except Album.DoesNotExist:
    #     raise Http404("Album does not exist.")
    # return render(request, 'music/detail.html', {'album': album})

    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'detail.html', {'album': album})


def favorite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        selected_song = album.song_set.get(pk=request.POST['song'])
    except(KeyError, Song.DoesNotExist):
        return render(request, 'detail.html', {
            'album' : album,
            'error_message': "You did not select a valid song",
        })
    else:
        selected_song.is_favorite = True
        selected_song.save()
        return render(request, 'detail.html', {'album': album})


# return REST
class ALbumList(APIView):

    def get(self, request: object) -> object:
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass

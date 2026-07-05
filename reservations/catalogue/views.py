from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Artist


def artist_index(request):
    artists = Artist.objects.all()
    return render(request, 'catalogue/artist_index.html', {'artists': artists})


def artist_show(request, id):
    artist = get_object_or_404(Artist, id=id)
    return render(request, 'catalogue/artist_show.html', {'artist': artist})
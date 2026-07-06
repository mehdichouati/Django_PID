from django.shortcuts import render, redirect, get_object_or_404
from .models import Artist
from .forms import ArtistForm


def artist_index(request):
    artists = Artist.objects.all()
    return render(request, 'catalogue/artist_index.html', {'artists': artists})


def artist_show(request, id):
    artist = get_object_or_404(Artist, id=id)
    return render(request, 'catalogue/artist_show.html', {'artist': artist})


def artist_create(request):
    form = ArtistForm()
    return render(request, 'catalogue/artist_form.html', {'form': form, 'title': 'Nouvel artiste'})


def artist_store(request):
    form = ArtistForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('artist_index')
    return render(request, 'catalogue/artist_form.html', {'form': form, 'title': 'Nouvel artiste'})


def artist_edit(request, id):
    artist = get_object_or_404(Artist, id=id)
    form = ArtistForm(instance=artist)
    return render(request, 'catalogue/artist_form.html', {'form': form, 'title': 'Modifier l\'artiste'})


def artist_update(request, id):
    artist = get_object_or_404(Artist, id=id)
    form = ArtistForm(request.POST, instance=artist)
    if form.is_valid():
        form.save()
        return redirect('artist_show', id=artist.id)
    return render(request, 'catalogue/artist_form.html', {'form': form, 'title': 'Modifier l\'artiste'})


def artist_delete(request, id):
    artist = get_object_or_404(Artist, id=id)
    artist.delete()
    return redirect('artist_index')
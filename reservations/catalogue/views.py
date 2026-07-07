from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Artist, Role, RoleUser, UserMeta
from .forms import ArtistForm, RegisterForm


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


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['login'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['firstname'],
                last_name=form.cleaned_data['lastname'],
                email=form.cleaned_data['email'],
            )
            UserMeta.objects.create(user=user, langue=form.cleaned_data['langue'])
            member_role = Role.objects.get(role='member')
            RoleUser.objects.create(user=user, role=member_role)
            messages.success(request, "Inscription réussie ! Vous pouvez maintenant vous connecter.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'catalogue/register.html', {'form': form})
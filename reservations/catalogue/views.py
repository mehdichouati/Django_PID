from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Artist, Role, RoleUser, UserMeta, Type, ArtisteType, Show, ArtisteTypeShow, Representation
from .forms import ArtistForm, RegisterForm, ShowForm


def artist_index(request):
    artists = Artist.objects.all()
    return render(request, 'catalogue/artist_index.html', {'artists': artists})


def artist_show(request, id):
    artist = get_object_or_404(Artist, id=id)
    artist_types = ArtisteType.objects.filter(artist=artist)
    available_types = Type.objects.exclude(id__in=artist_types.values_list('type_id', flat=True))
    return render(request, 'catalogue/artist_show.html', {
        'artist': artist,
        'artist_types': artist_types,
        'available_types': available_types,
    })


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


def artist_add_type(request, id):
    artist = get_object_or_404(Artist, id=id)
    if request.method == 'POST':
        type_id = request.POST.get('type_id')
        if type_id:
            type_obj = get_object_or_404(Type, id=type_id)
            ArtisteType.objects.get_or_create(artist=artist, type=type_obj)
            messages.success(request, f"Type '{type_obj}' ajouté à {artist}.")
    return redirect('artist_show', id=artist.id)


def artist_create_type(request, id):
    artist = get_object_or_404(Artist, id=id)
    if request.method == 'POST':
        type_name = request.POST.get('type_name', '').strip()
        if type_name:
            type_obj, created = Type.objects.get_or_create(type=type_name)
            ArtisteType.objects.get_or_create(artist=artist, type=type_obj)
            messages.success(request, f"Nouveau type '{type_name}' créé et ajouté à {artist}.")
        else:
            messages.error(request, "Le nom du type ne peut pas être vide.")
    return redirect('artist_show', id=artist.id)


def artist_remove_type(request, id, type_id):
    artist_type = get_object_or_404(ArtisteType, artist_id=id, type_id=type_id)
    artist_type.delete()
    messages.success(request, "Type retiré.")
    return redirect('artist_show', id=id)


def show_index(request):
    shows = Show.objects.all()
    return render(request, 'catalogue/show_index.html', {'shows': shows})


def show_show(request, id):
    show = get_object_or_404(Show, id=id)
    artist_types = ArtisteTypeShow.objects.filter(show=show).select_related('artiste_type__artist', 'artiste_type__type')
    representations = Representation.objects.filter(show=show)
    return render(request, 'catalogue/show_show.html', {
        'show': show,
        'artist_types': artist_types,
        'representations': representations,
    })


def show_create(request):
    form = ShowForm()
    return render(request, 'catalogue/show_form.html', {'form': form, 'title': 'Nouveau spectacle'})


def show_store(request):
    form = ShowForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('show_index')
    return render(request, 'catalogue/show_form.html', {'form': form, 'title': 'Nouveau spectacle'})


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
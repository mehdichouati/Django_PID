from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import (
    Artist, Role, RoleUser, UserMeta, Type, ArtisteType, Show, ArtisteTypeShow,
    Representation, Price, Reservation, RepresentationReservation
)
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

    # Recherche par mot-clé (titre)
    query = request.GET.get('q', '')
    if query:
        shows = shows.filter(Q(title__icontains=query))

    # Filtre par réservable
    bookable = request.GET.get('bookable', '')
    if bookable == '1':
        shows = shows.filter(bookable=True)
    elif bookable == '0':
        shows = shows.filter(bookable=False)

    # Tri
    sort = request.GET.get('sort', 'title')
    allowed_sorts = ['title', '-title', 'created_in', '-created_in']
    if sort in allowed_sorts:
        shows = shows.order_by(sort)
    else:
        shows = shows.order_by('title')

    # Pagination (10 par page, comme demandé par le PID)
    paginator = Paginator(shows, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalogue/show_index.html', {
        'page_obj': page_obj,
        'query': query,
        'bookable': bookable,
        'sort': sort,
    })


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


@login_required
def reservation_create(request, representation_id):
    representation = get_object_or_404(Representation, id=representation_id)
    prices = Price.objects.all()
    return render(request, 'catalogue/reservation_form.html', {
        'representation': representation,
        'prices': prices,
    })


@login_required
def reservation_store(request, representation_id):
    representation = get_object_or_404(Representation, id=representation_id)
    if request.method == 'POST':
        price_id = request.POST.get('price_id')
        quantity = request.POST.get('quantity', 1)
        price = get_object_or_404(Price, id=price_id)

        reservation = Reservation.objects.create(user=request.user, status='confirmed')
        RepresentationReservation.objects.create(
            representation=representation,
            reservation=reservation,
            price=price,
            quantity=quantity,
        )
        messages.success(request, "Réservation effectuée avec succès !")
        return redirect('my_reservations')
    return redirect('reservation_create', representation_id=representation.id)


@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'catalogue/my_reservations.html', {'reservations': reservations})
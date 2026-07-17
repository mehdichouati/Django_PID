import tablib
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.text import slugify
from django.db.models import Q, Avg, Prefetch
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .decorators import role_required
from .models import (
    Artist, Role, RoleUser, UserMeta, Type, ArtisteType, Show, ArtisteTypeShow,
    Representation, Price, Reservation, RepresentationReservation, Review, Location
)
from .forms import ArtistForm, RegisterForm, ShowForm, ReviewForm, ProfileForm


def is_user_admin(user):
    """Vérifie si l'utilisateur connecté a le rôle admin (ou est superuser)."""
    return user.is_authenticated and (
        user.is_superuser or
        RoleUser.objects.filter(user=user, role__role='admin').exists()
    )


def artist_index(request):
    artists = Artist.objects.all()
    return render(request, 'catalogue/artist_index.html', {
        'artists': artists,
        'is_admin': is_user_admin(request.user),
    })


def artist_show(request, id):
    artist = get_object_or_404(Artist, id=id)
    artist_types = ArtisteType.objects.filter(artist=artist)
    available_types = Type.objects.exclude(id__in=artist_types.values_list('type_id', flat=True))
    return render(request, 'catalogue/artist_show.html', {
        'artist': artist,
        'artist_types': artist_types,
        'available_types': available_types,
        'is_admin': is_user_admin(request.user),
    })


@role_required('admin')
def artist_create(request):
    form = ArtistForm()
    return render(request, 'catalogue/artist_form.html', {'form': form, 'title': 'Nouvel artiste'})


@role_required('admin')
def artist_store(request):
    form = ArtistForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('artist_index')
    return render(request, 'catalogue/artist_form.html', {'form': form, 'title': 'Nouvel artiste'})


@role_required('admin')
def artist_edit(request, id):
    artist = get_object_or_404(Artist, id=id)
    form = ArtistForm(instance=artist)
    return render(request, 'catalogue/artist_form.html', {'form': form, 'title': 'Modifier l\'artiste'})


@role_required('admin')
def artist_update(request, id):
    artist = get_object_or_404(Artist, id=id)
    form = ArtistForm(request.POST, instance=artist)
    if form.is_valid():
        form.save()
        return redirect('artist_show', id=artist.id)
    return render(request, 'catalogue/artist_form.html', {'form': form, 'title': 'Modifier l\'artiste'})


@role_required('admin')
def artist_delete(request, id):
    artist = get_object_or_404(Artist, id=id)
    artist.delete()
    return redirect('artist_index')


@role_required('admin')
def artist_add_type(request, id):
    artist = get_object_or_404(Artist, id=id)
    if request.method == 'POST':
        type_id = request.POST.get('type_id')
        if type_id:
            type_obj = get_object_or_404(Type, id=type_id)
            ArtisteType.objects.get_or_create(artist=artist, type=type_obj)
            messages.success(request, f"Type '{type_obj}' ajouté à {artist}.")
    return redirect('artist_show', id=artist.id)


@role_required('admin')
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


@role_required('admin')
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

    # Optimisation BDD : on précharge en une seule requête les représentations
    # futures de tous les spectacles affichés, au lieu d'une requête par spectacle (N+1)
    now = timezone.now()
    future_representations = Representation.objects.filter(schedule__gte=now).order_by('schedule')
    shows = shows.select_related('location').prefetch_related(
        Prefetch('representation_set', queryset=future_representations, to_attr='future_representations')
    )

    # Pagination (10 par page, comme demandé par le PID)
    paginator = Paginator(shows, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # La prochaine représentation est simplement la première de la liste préchargée
    for show in page_obj:
        show.next_representation = show.future_representations[0] if show.future_representations else None

    return render(request, 'catalogue/show_index.html', {
        'page_obj': page_obj,
        'query': query,
        'bookable': bookable,
        'sort': sort,
        'is_admin': is_user_admin(request.user),
    })


def show_export_csv(request):
    """Itération 7 - Progiciel tiers : export du catalogue en CSV via tablib."""
    shows = Show.objects.all()

    query = request.GET.get('q', '')
    if query:
        shows = shows.filter(Q(title__icontains=query))

    bookable = request.GET.get('bookable', '')
    if bookable == '1':
        shows = shows.filter(bookable=True)
    elif bookable == '0':
        shows = shows.filter(bookable=False)

    dataset = tablib.Dataset(headers=['Titre', 'Lieu', 'Année', 'Durée (min)', 'Réservable'])
    for show in shows:
        dataset.append([
            show.title,
            show.location.designation if show.location else '',
            show.created_in or '',
            show.duration or '',
            'Oui' if show.bookable else 'Non',
        ])

    response = HttpResponse(dataset.export('csv'), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="catalogue_spectacles.csv"'
    return response


@role_required('admin')
def show_import_csv(request):
    """Import de spectacles depuis un fichier CSV (même format que l'export)."""
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            messages.error(request, "Merci de sélectionner un fichier CSV.")
            return redirect('show_import_csv')

        try:
            data = csv_file.read().decode('utf-8')
            dataset = tablib.Dataset().load(data, format='csv')
        except Exception:
            messages.error(request, "Le fichier CSV n'a pas pu être lu. Vérifiez son format.")
            return redirect('show_import_csv')

        created_count = 0
        skipped_count = 0
        for row in dataset.dict:
            title = (row.get('Titre') or '').strip()
            location_name = (row.get('Lieu') or '').strip()

            if not title:
                skipped_count += 1
                continue

            slug = slugify(title)
            if Show.objects.filter(slug=slug).exists():
                skipped_count += 1
                continue

            location = Location.objects.filter(designation=location_name).first()
            bookable_value = str(row.get('Réservable') or '').strip().lower()

            Show.objects.create(
                title=title,
                slug=slug,
                location=location,
                created_in=row.get('Année') or None,
                duration=row.get('Durée (min)') or None,
                bookable=bookable_value in ['oui', 'yes', 'true', '1'],
            )
            created_count += 1

        messages.success(request, f"{created_count} spectacle(s) importé(s), {skipped_count} ignoré(s) (titre manquant ou doublon).")
        return redirect('show_index')

    return render(request, 'catalogue/show_import.html')


@cache_page(60)
def external_venues(request):
    """Itération 9 - Consommer une API publique externe (Open Data Ville de Bruxelles).
    Mise en cache 60s : évite de re-solliciter l'API externe à chaque visite."""
    url = 'https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/lieux_culturels_touristiques_evenementiels_visitbrussels_vbx/records'
    params = {'limit': 20}

    query = request.GET.get('q', '')
    if query:
        params['where'] = f'search(translations_fr_name, "{query}")'

    venues = []
    error = None
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        venues = data.get('results', [])
    except requests.RequestException:
        error = "Impossible de contacter l'API Open Data de Bruxelles pour le moment."

    return render(request, 'catalogue/external_venues.html', {
        'venues': venues,
        'query': query,
        'error': error,
        'is_admin': is_user_admin(request.user),
    })


@role_required('admin')
def sync_locations_from_opendata(request):
    """Mise à jour du catalogue (lieux) via le Web service tiers Open Data Bruxelles."""
    if request.method != 'POST':
        return redirect('external_venues')

    url = 'https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/lieux_culturels_touristiques_evenementiels_visitbrussels_vbx/records'
    params = {'limit': 20}

    created_count = 0
    updated_count = 0
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        venues = data.get('results', [])

        for venue in venues:
            name = (venue.get('translations_fr_name') or '').strip()
            if not name:
                continue

            designation = name[:60]
            slug = slugify(designation)[:60]
            address = venue.get('translations_fr_address_line1') or ''
            website = venue.get('translations_fr_website') or ''

            location, created = Location.objects.get_or_create(
                slug=slug,
                defaults={
                    'designation': designation,
                    'address': address,
                    'website': website,
                }
            )
            if created:
                created_count += 1
            else:
                location.address = address
                location.website = website
                location.save()
                updated_count += 1

        messages.success(request, f"Synchronisation terminée : {created_count} lieu(x) créé(s), {updated_count} mis à jour.")
    except requests.RequestException:
        messages.error(request, "Impossible de contacter l'API Open Data pour synchroniser le catalogue.")

    return redirect('external_venues')


def show_show(request, slug):
    show = get_object_or_404(Show, slug=slug)
    artist_types = ArtisteTypeShow.objects.filter(show=show).select_related('artiste_type__artist', 'artiste_type__type')
    representations = Representation.objects.filter(show=show)
    reviews = Review.objects.filter(show=show, validated=True).order_by('-created_at')
    average_stars = reviews.aggregate(Avg('stars'))['stars__avg']
    return render(request, 'catalogue/show_show.html', {
        'show': show,
        'artist_types': artist_types,
        'representations': representations,
        'reviews': reviews,
        'average_stars': average_stars,
        'review_form': ReviewForm(),
        'is_admin': is_user_admin(request.user),
    })


@role_required('admin')
def show_toggle_bookable(request, id):
    """Bascule le statut réservable d'un spectacle via AJAX (JSON), sans recharger la page."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    show = get_object_or_404(Show, id=id)
    show.bookable = not show.bookable
    show.save()
    return JsonResponse({'bookable': show.bookable})


@role_required('admin')
def show_bulk_delete(request):
    """Suppression groupée de spectacles sélectionnés via cases à cocher."""
    if request.method == 'POST':
        show_ids = request.POST.getlist('show_ids')
        if show_ids:
            deleted_count = Show.objects.filter(id__in=show_ids).count()
            Show.objects.filter(id__in=show_ids).delete()
            messages.success(request, f"{deleted_count} spectacle(s) supprimé(s).")
        else:
            messages.error(request, "Aucun spectacle sélectionné.")
    return redirect('show_index')


@login_required
def review_store(request, id):
    show = get_object_or_404(Show, id=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.show = show
            review.save()
            messages.success(request, "Votre avis a été soumis et sera visible après validation.")
        else:
            messages.error(request, "Merci de corriger les erreurs du formulaire.")
    return redirect('show_show', slug=show.slug)


@role_required('admin')
def show_create(request):
    form = ShowForm()
    return render(request, 'catalogue/show_form.html', {'form': form, 'title': 'Nouveau spectacle'})


@role_required('admin')
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
def profile_edit(request):
    user_meta, _ = UserMeta.objects.get_or_create(user=request.user, defaults={'langue': 'FR'})
    if request.method == 'POST':
        form = ProfileForm(request.POST, user=request.user)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            user_meta.langue = form.cleaned_data['langue']
            user_meta.affiliate_level = form.cleaned_data['affiliate_level']
            user_meta.save()
            messages.success(request, "Votre profil a été mis à jour.")
            return redirect('profile_edit')
    else:
        form = ProfileForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'langue': user_meta.langue,
            'affiliate_level': user_meta.affiliate_level,
        }, user=request.user)
    return render(request, 'catalogue/profile_form.html', {'form': form})


@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'catalogue/my_reservations.html', {'reservations': reservations})
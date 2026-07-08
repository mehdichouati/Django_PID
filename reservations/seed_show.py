import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings')
django.setup()

from catalogue.models import Locality, Location, Show, Artist, Type, ArtisteType, ArtisteTypeShow

# Localité
locality, _ = Locality.objects.get_or_create(postal_code="1170", locality="Watermael-Boitsfort")

# Lieu
location, _ = Location.objects.get_or_create(
    slug="delvaux",
    defaults={
        "locality": locality,
        "designation": "Espace Delvaux / La Vénerie",
        "address": "3 rue Gratès",
    }
)

# Spectacle Ayiti
show, _ = Show.objects.get_or_create(
    slug="ayiti",
    defaults={
        "location": location,
        "title": "Ayiti",
        "poster_url": "/wrapped/imgs/ayiti.jpg",
        "bookable": True,
        "created_in": 2012,
    }
)

# Récupération des artistes déjà créés
daniel = Artist.objects.get(firstname="Daniel", lastname="Marcelin")
philippe = Artist.objects.get(firstname="Philippe", lastname="Laurent")

# Types
auteur = Type.objects.get(type="Auteur")
scenographe = Type.objects.get(type="Scénographe")

# Liaisons artist-type
at_daniel_auteur, _ = ArtisteType.objects.get_or_create(artist=daniel, type=auteur)
at_philippe_auteur, _ = ArtisteType.objects.get_or_create(artist=philippe, type=auteur)
at_daniel_sceno, _ = ArtisteType.objects.get_or_create(artist=daniel, type=scenographe)

# Liaisons avec le spectacle
ArtisteTypeShow.objects.get_or_create(artiste_type=at_daniel_auteur, show=show)
ArtisteTypeShow.objects.get_or_create(artiste_type=at_philippe_auteur, show=show)
ArtisteTypeShow.objects.get_or_create(artiste_type=at_daniel_sceno, show=show)

print("Spectacle 'Ayiti' créé avec succès, avec ses artistes et lieu !")
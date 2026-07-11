import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings')
django.setup()

from catalogue.models import Location, Show, Artist, Type, ArtisteType, ArtisteTypeShow, Representation
from datetime import datetime

# Lieux supplémentaires
belfius, _ = Location.objects.get_or_create(
    slug="belfius-art-collection",
    defaults={"designation": "Belfius Art Collection"}
)
samaritaine, _ = Location.objects.get_or_create(
    slug="la-samaritaine",
    defaults={"designation": "La Samaritaine"}
)

# Artistes supplémentaires
bob, _ = Artist.objects.get_or_create(firstname="Bob", lastname="Sull")
marc, _ = Artist.objects.get_or_create(firstname="Marc", lastname="Flynn")

# Type Auteur (déjà existant normalement)
auteur, _ = Type.objects.get_or_create(type="Auteur")

# Spectacle 2 : Ceci N'est Pas Un Chanteur Belge
show2, _ = Show.objects.get_or_create(
    slug="ceci-nest-pas-un-chanteur-belge",
    defaults={
        "location": belfius,
        "title": "Ceci N'est Pas Un Chanteur Belge",
        "bookable": False,
        "created_in": 2018,
    }
)
Representation.objects.get_or_create(
    show=show2, location=belfius,
    schedule=datetime(2018, 3, 15, 20, 30)
)

# Spectacle 3 : Cible Mouvante
show3, _ = Show.objects.get_or_create(
    slug="cible-mouvante",
    defaults={
        "location": samaritaine,
        "title": "Cible Mouvante",
        "bookable": True,
        "created_in": 2018,
    }
)
at_marc, _ = ArtisteType.objects.get_or_create(artist=marc, type=auteur)
ArtisteTypeShow.objects.get_or_create(artiste_type=at_marc, show=show3)

Representation.objects.get_or_create(
    show=show3, location=samaritaine,
    schedule=datetime(2018, 4, 10, 20, 0)
)
Representation.objects.get_or_create(
    show=show3, location=samaritaine,
    schedule=datetime(2018, 4, 12, 20, 0)
)

print("Spectacles supplémentaires créés avec succès !")
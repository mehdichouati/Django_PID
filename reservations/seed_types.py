import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings')
django.setup()

from catalogue.models import Type

Type.objects.create(type="Auteur")
Type.objects.create(type="Metteur en scène")
Type.objects.create(type="Comédien")
Type.objects.create(type="Scénographe")
Type.objects.create(type="Technicien")

print("Types créés avec succès !")
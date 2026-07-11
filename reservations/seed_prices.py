import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservations.settings')
django.setup()

from catalogue.models import Price
from datetime import date

Price.objects.get_or_create(
    type="Plein tarif",
    defaults={"price": 15.00, "start_date": date(2024, 1, 1), "end_date": date(2030, 12, 31)}
)
Price.objects.get_or_create(
    type="Tarif réduit",
    defaults={"price": 10.00, "start_date": date(2024, 1, 1), "end_date": date(2030, 12, 31)}
)

print("Tarifs créés avec succès !")
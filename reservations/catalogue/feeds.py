from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils import timezone
from .models import Representation


class UpcomingRepresentationsFeed(Feed):
    title = "Projet Réservations — Prochaines représentations"
    link = "/show/"
    description = "Flux RSS des prochaines représentations de spectacles à venir."

    def items(self):
        return Representation.objects.filter(
            schedule__gte=timezone.now()
        ).select_related('show', 'location').order_by('schedule')[:20]

    def item_title(self, item):
        return f"{item.show.title} — {item.schedule.strftime('%d/%m/%Y %H:%M')}"

    def item_description(self, item):
        location_name = item.location.designation if item.location else (
            item.show.location.designation if item.show.location else "lieu non précisé"
        )
        return f"Représentation de « {item.show.title} » le {item.schedule.strftime('%d/%m/%Y à %H:%M')} à {location_name}."

    def item_link(self, item):
        return reverse('show_show', args=[item.show.slug])
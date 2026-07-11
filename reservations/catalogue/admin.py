from django.contrib import admin
from .models import (
    Artist, Role, RoleUser, UserMeta, Type, ArtisteType,
    Locality, Location, Show, ArtisteTypeShow, Representation,
    Price, Reservation, RepresentationReservation, Review
)

admin.site.register(Artist)
admin.site.register(Role)
admin.site.register(RoleUser)
admin.site.register(UserMeta)
admin.site.register(Type)
admin.site.register(ArtisteType)
admin.site.register(Locality)
admin.site.register(Location)
admin.site.register(Show)
admin.site.register(ArtisteTypeShow)
admin.site.register(Representation)
admin.site.register(Price)
admin.site.register(Reservation)
admin.site.register(RepresentationReservation)
admin.site.register(Review)
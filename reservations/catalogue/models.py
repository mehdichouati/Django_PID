from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    firstname = models.CharField(max_length=60)
    lastname = models.CharField(max_length=60)

    class Meta:
        db_table = 'artists'

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Role(models.Model):
    role = models.CharField(max_length=30)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.role


class RoleUser(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='role_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')

    class Meta:
        db_table = 'role_user'


class UserMeta(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='meta')
    langue = models.CharField(max_length=2, default='FR')

    class Meta:
        db_table = 'user_meta'

    def __str__(self):
        return f"Meta de {self.user.username}"


class Type(models.Model):
    type = models.CharField(max_length=60)

    class Meta:
        db_table = 'types'

    def __str__(self):
        return self.type


class ArtisteType(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, db_column='artist_id')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, db_column='type_id')

    class Meta:
        db_table = 'artiste_type'

    def __str__(self):
        return f"{self.artist} - {self.type}"


class Locality(models.Model):
    postal_code = models.CharField(max_length=6, unique=True)
    locality = models.CharField(max_length=60, unique=True)

    class Meta:
        db_table = 'localities'

    def __str__(self):
        return f"{self.postal_code} {self.locality}"


class Location(models.Model):
    locality = models.ForeignKey(Locality, on_delete=models.SET_NULL, null=True, blank=True, db_column='locality_id')
    slug = models.SlugField(max_length=60, unique=True)
    designation = models.CharField(max_length=60)
    address = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'locations'

    def __str__(self):
        return self.designation


class Show(models.Model):
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, db_column='location_id')
    slug = models.SlugField(max_length=60, unique=True)
    title = models.CharField(max_length=255)
    poster_url = models.CharField(max_length=255, blank=True, null=True)
    duration = models.PositiveSmallIntegerField(blank=True, null=True)
    created_in = models.PositiveSmallIntegerField(blank=True, null=True)
    bookable = models.BooleanField(default=False)

    class Meta:
        db_table = 'shows'

    def __str__(self):
        return self.title


class ArtisteTypeShow(models.Model):
    artiste_type = models.ForeignKey(ArtisteType, on_delete=models.CASCADE, db_column='artiste_type_id')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, db_column='show_id')

    class Meta:
        db_table = 'artiste_type_show'

    def __str__(self):
        return f"{self.artiste_type} - {self.show}"


class Representation(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, db_column='show_id')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, db_column='location_id')
    schedule = models.DateTimeField()

    class Meta:
        db_table = 'representations'

    def __str__(self):
        return f"{self.show} - {self.schedule}"


class Price(models.Model):
    type = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'prices'

    def __str__(self):
        return f"{self.type} - {self.price}€"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=60, default='pending')

    class Meta:
        db_table = 'reservations'

    def __str__(self):
        return f"Réservation #{self.id} - {self.user}"


class RepresentationReservation(models.Model):
    representation = models.ForeignKey(Representation, on_delete=models.CASCADE, db_column='representation_id')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, db_column='reservation_id')
    price = models.ForeignKey(Price, on_delete=models.CASCADE, db_column='price_id')
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table = 'representation_reservation'

    def __str__(self):
        return f"{self.representation} x{self.quantity}"
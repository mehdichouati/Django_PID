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
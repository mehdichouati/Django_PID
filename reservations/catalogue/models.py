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
from django.db import models

#
#
from login_app.models import User


# Vehicles group
class Veh_type(models.Model):
    group = models.CharField(max_length=20)

    def __str__(self):
        return self.group


# Vehicles models
class Vehicles_table(models.Model):
    # id =
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owned_vehicles')

    name = models.CharField(max_length=128)
    photo_URL = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    localization = models.CharField(max_length=128)
    group = models.ForeignKey(Veh_type, on_delete=models.PROTECT)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_rented = models.BooleanField(default=False)
    rent_start = models.DateTimeField(null=True)
    currently_rented_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None,
                                            related_name='rented_vehicles')

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


# Comments table
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicles_table, on_delete=models.CASCADE)
    text = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[0:50]

from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Vehicles_table)
admin.site.register(models.Comments)
admin.site.register(models.Veh_type)

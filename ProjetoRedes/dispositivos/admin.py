from django.contrib import admin
from .models import modeloDispositivo


@admin.register(modeloDispositivo)
class CategoriaAdmin(admin.ModelAdmin):
    pass
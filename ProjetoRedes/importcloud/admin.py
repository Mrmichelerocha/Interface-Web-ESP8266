from django.contrib import admin
from .models import modeloDatabase

# Register your models here.

@admin.register(modeloDatabase)
class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('data', 'horarioi', 'horariof', 'status', 'decorrido', 'dispositivo')


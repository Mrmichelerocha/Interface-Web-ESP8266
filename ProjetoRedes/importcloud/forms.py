from django.forms import ModelForm
from importcloud.models import modeloDatabase


class modeloDatabaseForm(ModelForm):
    class Meta:
        model = modeloDatabase
        fields = ['data', 'horarioi', 'horariof', 'status', 'decorrido', 'dispositivo']
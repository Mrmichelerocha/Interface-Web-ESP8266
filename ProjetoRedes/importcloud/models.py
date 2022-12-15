from django.db import models
from dispositivos.models import modeloDispositivo

# Create your models here.

class modeloDatabase(models.Model):
    data = models.DateField()
    horarioi = models.TimeField()
    horariof = models.TimeField()
    status = models.FloatField()
    decorrido = models.IntegerField()
    dispositivo = models.ForeignKey(modeloDispositivo, on_delete=models.DO_NOTHING, null=True)

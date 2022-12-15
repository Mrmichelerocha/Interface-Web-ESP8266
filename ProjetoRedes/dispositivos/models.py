from django.db import models

# Create your models here.

class modeloDispositivo(models.Model):
    nome = models.CharField(max_length=150, null=True)
    objetivo = models.CharField(max_length=150, null=True)
    urlcloud = models.CharField(max_length=300, null=True)

    def __str__(self) -> str:
        return self.nome

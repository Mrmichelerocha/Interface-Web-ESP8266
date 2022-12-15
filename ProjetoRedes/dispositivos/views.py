from django.shortcuts import render
from .models import modeloDispositivo
from importcloud.models import modeloDatabase
from django.core.paginator import Paginator
import pandas as pd

def dispositivos(request):
    data = {}
    data['db'] = modeloDispositivo.objects.all()
    return render(request, 'dispositivos.html', data)

def coisa(request):
    coisa = modeloDatabase.objects.all()
    coisa_paginator = Paginator(coisa, 10)
    page_num = request.GET.get('page')
    page = coisa_paginator.get_page(page_num)
    return render(request, 'coisa.html', {'page': page})

def pandas(request):
    item = modeloDatabase.objects.all().values()
    df = pd.DataFrame(item)

    tempo_decorrido = df['decorrido']


    if item == '1':
        t_decorrido = sum(tempo_decorrido)
        df['decorrido'] = t_decorrido

    elif item == '2':
        t_decorrido = sum(tempo_decorrido)
        df['decorrido'] = t_decorrido

    dia_decorrido = df[['data', 'status', 'dispositivo_id', 'decorrido']].groupby(['data', 'status', 'dispositivo_id']).sum()

    mydict = {
        "df": dia_decorrido.to_html(),
        "data": df['data'],
        "decorrido": df['decorrido'],
    }

    return render(request, 'pandas.html', context=mydict)
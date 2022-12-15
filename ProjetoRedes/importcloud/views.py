from doctest import OutputChecker
import json
from django.shortcuts import render, redirect
from importcloud.models import modeloDatabase
from dispositivos.models import modeloDispositivo
from importcloud.forms import modeloDatabaseForm
from django.http import JsonResponse
from django.http import HttpResponse
import datetime
from datetime import datetime, date
import requests
from dateutil import parser
import dateutil
import sqlite3

# Create your views here.

def database(request):
    data = {}
    data['db'] = modeloDatabase.objects.all()
    return render(request, 'database.html', data)


def form(request):
    data = {}
    data['form'] = modeloDatabaseForm()
    return render(request, 'form.html', data)

def create(request):
    form = modeloDatabaseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('home')

def view(request, pk):
    data = {}
    data['db'] = modeloDatabase.objects.get(pk=pk)
    return render(request, 'view.html', data)

def edit(request, pk):
    data = {}
    data['db'] = modeloDatabase.objects.get(pk=pk)
    data['form'] = modeloDatabaseForm(instance=data['db'])
    return render(request,'form.html',data)

def update(request, pk):
    data = {}
    data['db'] = modeloDatabase.objects.get(pk=pk)
    form = modeloDatabaseForm(request.POST or None, instance=data['db'])
    if form.is_valid():
        form.save()
        return redirect('home')

def delete(request, pk):
    db = modeloDatabase.objects.get(pk=pk)
    db.delete()
    return redirect('home')

def importdb(request): 
    data = {}
    data = modeloDispositivo.objects.all()

    # for e in modeloDatabase.objects.all():
    #     print(e.dispositivo.urlcloud)

    urlcloud = data[0].urlcloud
    dispositivo = data[0].pk
    print("filde 1")
    print(dispositivo)

    r = requests.get(urlcloud)
    dic_requisicao = r.json()
    i = 0
    j = 1
    

    while i < len(dic_requisicao['feeds']):
        if i == len(dic_requisicao['feeds'])-1 :
            break
        else:
            # extrai hora inicio e datat inicio
            dic_horai = dateutil.parser.parse(dic_requisicao['feeds'][i]['created_at'])
            if dic_horai is not None:
                timei = dic_horai.time()
                datai = dic_horai.date()
            else:
                print('variable stores a None value')


            # extrai hora final e data final 
            dic_horaf = dateutil.parser.parse(dic_requisicao['feeds'][j]['created_at'])
            if dic_horaf is not None:
                timef = dic_horaf.time()
                dataf = dic_horaf.date()
            else:
                print('variable stores a None value')

            

            #  extrai o status 
            dic_status = dic_requisicao['feeds'][i]['field1']
            if dic_status is not None:
                status = float(dic_status)
            else:
                print('variable stores a None value')

            #  calcula o tempo decorrido 
            d1 = int(datai.strftime("%d"))
            d2 = int(dataf.strftime("%d"))
            mes1 = int(datai.strftime("%m"))
            mes2 = int(dataf.strftime("%m"))
            y1 = int(datai.strftime("%Y"))
            y2 = int(dataf.strftime("%Y"))
            
            h1 = int(timei.strftime("%H"))
            h2 = int(timef.strftime("%H"))
            min1 = int(timei.strftime("%M"))
            min2 = int(timef.strftime("%M"))
            s1 = int(timei.strftime("%S"))
            s2 = int(timef.strftime("%S"))

            dic_decorrido = tempo_decorrido(d1, mes1, y1, d2, mes2, y2, h1, min1, s1, h2, min2, s2)

            i+=1
            j+=1

            insertVaribleIntoTable(i, datai, timei, timef, status, dic_decorrido, dispositivo)

    return HttpResponse(r.text)

def importdb2(request): 
    data = {}
    data = modeloDispositivo.objects.all()

    # for e in modeloDatabase.objects.all():
    #     print(e.dispositivo.urlcloud)

    urlcloud = data[1].urlcloud
    dispositivo = data[1].pk
    print("filde 2")
    print(dispositivo)
    r = requests.get(urlcloud)
    dic_requisicao = r.json()
    print(json.dumps(dic_requisicao, indent=4))
    i = 0
    j = 1
    

    while i < len(dic_requisicao['feeds']):
        if i == len(dic_requisicao['feeds'])-1 :
            break
        else:
            # extrai hora inicio e datat inicio
            dic_horai = dateutil.parser.parse(dic_requisicao['feeds'][i]['created_at'])
            if dic_horai is not None:
                timei = dic_horai.time()
                datai = dic_horai.date()
            else:
                print('variable stores a None value')


            # extrai hora final e data final 
            dic_horaf = dateutil.parser.parse(dic_requisicao['feeds'][j]['created_at'])
            if dic_horaf is not None:
                timef = dic_horaf.time()
                dataf = dic_horaf.date()
            else:
                print('variable stores a None value')

            
            status = 0
            #  extrai o status 
            dic_status = dic_requisicao['feeds'][i]['field2']
            if dic_status is not None:
                status = float(dic_status)
            else:
                print('variable stores a None value')

            #  calcula o tempo decorrido 
            d1 = int(datai.strftime("%d"))
            d2 = int(dataf.strftime("%d"))
            mes1 = int(datai.strftime("%m"))
            mes2 = int(dataf.strftime("%m"))
            y1 = int(datai.strftime("%Y"))
            y2 = int(dataf.strftime("%Y"))
            
            h1 = int(timei.strftime("%H"))
            h2 = int(timef.strftime("%H"))
            min1 = int(timei.strftime("%M"))
            min2 = int(timef.strftime("%M"))
            s1 = int(timei.strftime("%S"))
            s2 = int(timef.strftime("%S"))

            dic_decorrido = tempo_decorrido(d1, mes1, y1, d2, mes2, y2, h1, min1, s1, h2, min2, s2)

            i+=1
            j+=1

            insertVaribleIntoTable(i + len(dic_requisicao['feeds']) - 1, datai, timei, timef, status, dic_decorrido, dispositivo)

    return HttpResponse(r.text)

def tempo_decorrido (d1, mes1, y1, d2, mes2, y2, h1, min1, s1, h2, min2, s2):

    decorrido_dia = d2 - d1
    decorrido_mes = mes2 - mes1
    decorrido_ano = y2 - y1

    decorrido_hora = h2 - h1
    decorrido_minuto = min2 - min1
    decorrido_segundo = s2 - s1


    # If final day < initial day, resolve month difference
    if d2 < d1:
        if mes1 == 1 or mes1 == 3 or mes1 == 5 or mes1 == 7 or mes1 == 8 or mes1 == 10 or mes1 == 12:
            d1 = 31 - d1
            decorrido_dia = d1 + d2
        elif mes1 == 4 or mes1 == 6 or mes1 == 9 or mes1 == 11:
            d1 = 30 - d1
            decorrido_dia = d1 + d2
        else:
            d1 = 28 - d1
            decorrido_dia = d1 + d2
    
    # Resolve difference of year
    if mes2 < mes1:
        mes1 = 12 - mes1
        decorrido_mes = mes1 + mes2

    # Resolve difference of hour
    if h2 < h1:
        h1 = 24 - h1
        decorrido_hora = h1 + h2
    if min2 < min1:
        min1 = 60 - min1
        decorrido_minuto = min1 + min2
    if s2 < s1:
        s1 = 60 - s1
        decorrido_segundo = s1 + s2
    
    # Filling decorrido with datetime variables in minutos
    ano_decorrido = decorrido_ano * 525600
    mes_decorrido = decorrido_mes * 43800
    dia_decorrido = decorrido_dia * 1440

    hora_decorrido = decorrido_hora * 60
    minuto_decorrido = decorrido_minuto
    segundo_decorrido = decorrido_segundo / 60

    decorrido = (ano_decorrido + mes_decorrido + dia_decorrido +
                hora_decorrido + minuto_decorrido + segundo_decorrido)

    return decorrido

def insertVaribleIntoTable(var_id, data, horarioi, horariof, status, decorrido, dispositivo):
    try:
        sqliteConnection = sqlite3.connect('db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        cursor.execute("insert or ignore into importcloud_modelodatabase values (?, ?, ?, ?, ?, ?, ?)", (int(var_id), str(data), str(horarioi), str(horariof), int(status), str(decorrido), int(dispositivo)))
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")



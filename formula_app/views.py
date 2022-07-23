import json
# import threading
# for thread in threading.enumerate(): 
        #     print(thread.name)
from threading import Thread
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from formula_app.scrapers.standings import get_driver_standings, get_constructor_standings, get_races
from formula_app.scrapers import telma, sportskimk, sporteden
from .models import Tim, Vest, Vozac, Trka

"""
    dataJson so go ima u sekoj context dict 
    e za js skriptata so meste u navbar koja trka e sledna
    TODO: ako e sredeno countdown.js da rabote od static proveri dali moze da se poednostave tuka
    TODO: toa dataJSON treba da se naprae da zima od database a ne od JSON so ima zacuvuvano od porano
"""

def home(request):
    data = {}
    with open("formula_app/data/trki/trki.json", 'r') as read_file:
        data = json.load(read_file)
    
    dataJSON = json.dumps(data)
    context = {
        "data": dataJSON
    }

    return render(request, 'formula_app/odbrojuvanje.html', context)


def novosti(request):
    # telma.scrape()
    # sportskimk.scrape()
    # sporteden.scrape()

    data = {}
    with open("formula_app/data/trki/trki.json", 'r') as read_file:
        data = json.load(read_file)
    
    dataJSON = json.dumps(data)

    # "-skrejp_datum" e rastecki a samo "skrejpy_datum" e opagjacki
    # ili obratno proveri koa ke scrape nes nova vest
    vesti = Vest.objects.all().order_by("-skrejp_datum")
    
    context = {
        "veesti": vesti,
        "data": dataJSON,
    }

    return render(request, 'formula_app/novosti.html', context)


def plasman(request):
    # get_constructor_standings()
    # get_driver_standings()
    # get_races()
    data = {}
    with open("formula_app/data/trki/trki.json", 'r') as read_file:
        data = json.load(read_file)
    
    dataJSON = json.dumps(data)
    vozaci = Vozac.objects.all()
    timovi = Tim.objects.all().filter(~Q(ime="default"))

    context = {
        "vozaci": vozaci,
        "timovi": timovi,
        "data": dataJSON,
    }

    return render(request, 'formula_app/plasman.html', context)


def plasman_OLD(request):
    vozaci = []
    with open("formula_app/data/plasman/vozaci-plasman.json", 'r') as read_file:
        vozaci = json.load(read_file)["results"]

    data = {}
    with open("formula_app/data/trki/trki.json", 'r') as read_file:
        data = json.load(read_file)
    
    dataJSON = json.dumps(data)
    
    context = {
        "vozaci": vozaci,
        "data": dataJSON,
    }

    return render(request, 'formula_app/plasman.html', context)


def raspored(request):
    # trki = []
    # with open("formula_app/data/trki/trki.json", 'r') as read_file:
    #     trki = json.load(read_file)["results"]
    
    data = {}
    with open("formula_app/data/trki/trki.json", 'r') as read_file:
        data = json.load(read_file)
    
    dataJSON = json.dumps(data)
    trki = Trka.objects.all()
    # print(trki.sesii)
    context = {
        "trki": trki,
        "data": dataJSON,
    }

    return render(request, 'formula_app/raspored.html', context)


def traka_info(request, traka_id):
    if request.method == "GET":
        trki = []
        with open("formula_app/data/trki/trki.json", 'r') as read_file:
            trki = json.load(read_file)["results"]
        
    data = {}
    with open("formula_app/data/trki/trki.json", 'r') as read_file:
        data = json.load(read_file)
    
    dataJSON = json.dumps(data)
        
    # TODO
    # tuka nekakov exception treba za ako ne ja najde taa trka u json
    # so ne treba da se sluce nikogas zatoa so od isti json zimat datata
    # ama za sekoj slucaj
    context = {}
    for i in trki:
        if int(i['race_id']) == int(traka_id):
            context = {
                "traka": i,
                "data": dataJSON,
            }

    return render(request, 'formula_app/traka-info.html', context)



def otvorena_novost(request, novost_id):
    if request.method == "GET":
        telma_data = []
        with open("formula_app/data/vesti/telma.json", 'r') as read_file:
            telma_data = json.load(read_file)
        
    data = {}
    with open("formula_app/data/trki/trki.json", 'r') as read_file:
        data = json.load(read_file)
    
    dataJSON = json.dumps(data)
    selektirana_vest = Vest.objects.get(custom_id=novost_id)
    
    context = {}
    # for i in telma_data:
    #     if i['id'] == novost_id:
    #         context = {
    #             "novost": i,
    #             "data": dataJSON,
    #         }

    context = {
                "novost": selektirana_vest,
                "data": dataJSON,
            }

    return render(request, 'formula_app/otvorena-vest.html', context)


def gledaj(request):
    return render(request, 'formula_app/strimanje.html')


@staff_member_required()
def manage(request):
    if(request.GET.get('update_driver_standings')):
        thread_driver_update = Thread(target=get_driver_standings, name="driv")
        thread_driver_update.start()
        thread_driver_update.join()
    if(request.GET.get('update_team_standings')):
        thread_constructor_update = Thread(target=get_constructor_standings, name="constr")
        thread_constructor_update.start()
        thread_constructor_update.join()
    if(request.GET.get('update_races')):
        thread_races_update = Thread(target=get_races, name="upd_races")
        thread_races_update.start()
        thread_races_update.join()
    if(request.GET.get('update_telma_vesti')):
        thread_telma_vesti = Thread(target=telma.scrape(), name="telma_scrape")
        thread_telma_vesti.start()
        thread_telma_vesti.join()
    if(request.GET.get('update_sportskimk_vesti')):
        thread_sportskimk_vesti = Thread(target=sportskimk.scrape(), name="sportskimk_scrape")
        thread_sportskimk_vesti.start()
        thread_sportskimk_vesti.join()
    if(request.GET.get('update_sporteden_vesti')):
        thread_sporteden_vesti = Thread(target=sporteden.scrape(), name="sporteden_scrape")
        thread_sporteden_vesti.start()
        thread_sporteden_vesti.join()
    return render(request, 'formula_app/manage.html')

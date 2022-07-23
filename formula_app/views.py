import json
from threading import Thread
import traceback
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from requests import request
from formula_app.forms import NewUserForm
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


def raspored(request):
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
    data = {}
    with open("formula_app/data/trki/trki.json", 'r') as read_file:
        data = json.load(read_file)
    
    dataJSON = json.dumps(data)
    selektirana_vest = Vest.objects.get(custom_id=novost_id)

    context = {
        "novost": selektirana_vest,
        "data": dataJSON,
    }

    return render(request, 'formula_app/otvorena-vest.html', context)


@login_required()
def gledaj(request):
    return render(request, 'formula_app/strimanje.html')


@staff_member_required()
def manage(request):
    context = dict()
    if(request.GET.get('update_driver_standings')):
        try:
            status = get_driver_standings()
            context = {
                "status_message": status,
            }
        except Exception as e:
            tb = traceback.format_exc()
            context = {
                "status_message": tb,
            }
        
    if(request.GET.get('update_team_standings')):
        try:
            status = get_constructor_standings()
            context = {
                "status_message": status,
            }
        except Exception as e:
            tb = traceback.format_exc()
            context = {
                "status_message": tb,
            }

    if(request.GET.get('update_races')):
        try:
            status = get_races()
            context = {
                "status_message": status,
            }
        except Exception as e:
            tb = traceback.format_exc()
            context = {
                "status_message": tb,
            }

    if(request.GET.get('update_telma_vesti')):
        try:
            status = telma.scrape()
            context = {
                "status_message": status,
            }
        except Exception as e:
            tb = traceback.format_exc()
            context = {
                "status_message": tb,
            }

    if(request.GET.get('update_sportskimk_vesti')):
        try:
            status = sportskimk.scrape()
            context = {
                "status_message": status,
            }
        except Exception as e:
            tb = traceback.format_exc()
            context = {
                "status_message": tb,
            }

    if(request.GET.get('update_sporteden_vesti')):
        try:
            status = sporteden.scrape()
            context = {
                "status_message": status,
            }
        except Exception as e:
            tb = traceback.format_exc()
            context = {
                "status_message": tb,
            }

    return render(request, 'formula_app/manage.html', context=context)


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("formula_app:app-welcome")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="formula_app/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("formula_app:app-welcome")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="formula_app/login.html", context={"login_form":form})


def welcome(request):
    return render(request, 'formula_app/welcome.html')

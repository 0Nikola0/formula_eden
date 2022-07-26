import datetime
from django.utils import timezone
import traceback
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from formula_app.scrapers.standings import get_driver_standings, get_constructor_standings, get_races
from formula_app.scrapers import telma, sportskimk, sporteden
from .models import Tim, Vest, Vozac, Trka
from formula_app.forms import NewUserForm


def home(request):
    sledna_trka = Trka.objects.filter(pocetok__gte=datetime.datetime.now()).order_by("pocetok").first()
    sledna_sesija = sledna_trka.sesii.all().filter(datum__gte=timezone.now()).order_by("datum").first()
    context = {
        "sledna_trka": sledna_trka,
        "sledna_sesija": sledna_sesija,
    }

    return render(request, 'formula_app/odbrojuvanje.html', context)


def novosti(request):
    # "-skrejp_datum" e rastecki a samo "skrejpy_datum" e opagjacki
    # ili obratno proveri koa ke scrape nes nova vest
    vesti = Vest.objects.all().order_by("-skrejp_datum")
    sledna_trka = Trka.objects.filter(pocetok__gte=datetime.datetime.now()).order_by("pocetok").first()
    
    context = {
        "veesti": vesti,
        "sledna_trka": sledna_trka,
    }

    return render(request, 'formula_app/novosti.html', context)


def plasman(request):
    sledna_trka = Trka.objects.filter(pocetok__gte=datetime.datetime.now()).order_by("pocetok").first()
    vozaci = Vozac.objects.all()
    timovi = Tim.objects.all().filter(~Q(ime="default"))

    context = {
        "vozaci": vozaci,
        "timovi": timovi,
        "sledna_trka": sledna_trka,
    }

    return render(request, 'formula_app/plasman.html', context)


def raspored(request):
    trki = Trka.objects.all()
    sledna_trka = Trka.objects.filter(pocetok__gte=datetime.datetime.now()).order_by("pocetok").first()

    context = {
        "trki": trki,
        "sledna_trka": sledna_trka,
    }

    return render(request, 'formula_app/raspored.html', context)


def traka_info(request, traka_id): 
    trki = Trka.objects.all()
    selektirana_trka = trki.filter(race_id=traka_id).first()
    sledna_trka = trki.filter(pocetok__gte=datetime.datetime.now()).order_by("pocetok").first()

    context = {
        "sledna_trka": sledna_trka,
        "traka": selektirana_trka,
    }

    return render(request, 'formula_app/traka-info.html', context)


def otvorena_novost(request, novost_naslov):
    sledna_trka = Trka.objects.filter(pocetok__gte=datetime.datetime.now()).order_by("pocetok").first()
    selektirana_vest = Vest.objects.all().filter(naslov=novost_naslov).first()
    vesti = Vest.objects.all().order_by('-skrejp_datum')[:2]

    context = {
        "sledna_trka": sledna_trka,
        "novost": selektirana_vest,
        "vesti": vesti,
    }

    return render(request, 'formula_app/otvorena-vest.html', context)


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
    sledna_trka = Trka.objects.filter(pocetok__gte=datetime.datetime.now()).order_by("pocetok").first()
    context["sledna_trka"] = sledna_trka

    return render(request, 'formula_app/manage.html', context=context)


# Treba REDIRECT da se srede za da rabote ovoa dobro so u.is_auth
# @user_passes_test(lambda u: not u.is_authenticated)
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

    sledna_trka = Trka.objects.filter(pocetok__gte=datetime.datetime.now()).order_by("pocetok").first()
    context = {
        "register_form":form,
        "sledna_trka": sledna_trka,
    }

    return render (request=request, template_name="formula_app/register.html", context=context)


# @user_passes_test(lambda u: not u.is_authenticated)
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

    sledna_trka = Trka.objects.filter(pocetok__gte=datetime.datetime.now()).order_by("pocetok").first()
    context = {
        "login_form":form,
        "sledna_trka": sledna_trka,
    }

    return render(request=request, template_name="formula_app/login.html", context=context)


def welcome(request):
    return render(request, 'formula_app/welcome.html')

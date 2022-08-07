from unittest.util import _MAX_LENGTH
from django.db import models
from django.utils import timezone
import datetime


class Tim(models.Model):
    ime = models.CharField(max_length=50)
    pozicija = models.IntegerField(default=0)
    poeni = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.ime}"


def get_placeholder_team():
    '''
    Za da moze da ima default vrednost Vozac.tim
    ne treba uopste da ima potreba od ovoa osven ako ne dodadat nov vozac mid-season
    '''
    return Tim.objects.get_or_create(ime="default")[0]


# TODO isto i za ZNAME kako so e za SLIKA
class Vozac(models.Model):
    ime = models.CharField(max_length=30)
    prezime = models.CharField(max_length=30)
    pozicija = models.IntegerField(default=0)
    poeni = models.IntegerField(default=0)
    tim = models.ForeignKey(Tim, on_delete=models.SET(get_placeholder_team), default=get_placeholder_team)
    drzava = models.CharField(max_length=80)
    slika = models.CharField(max_length=30, default="nema-slika")

    def __str__(self):
        return f"{self.ime} {self.prezime}"
    

# =================================================================== #

class Sesija(models.Model):
    session_id = models.IntegerField(default=0)
    ime = models.TextField()
    trka_ime = models.TextField()
    datum = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return f"{self.session_id} {self.ime}"


class Trka(models.Model):
    race_id = models.IntegerField()
    status = models.TextField()
    ime = models.TextField()
    drzava = models.TextField()
    staza = models.TextField()
    pocetok = models.DateField(default=datetime.datetime.now().strftime('%Y-%m-%d'))
    kraj = models.DateField(default=datetime.datetime.now().strftime('%Y-%m-%d'))
    sesii = models.ManyToManyField(Sesija, through='TrkaSesija', through_fields=('trka', 'sesija'), blank=True)
    staza_slika = models.TextField(default="nema")
    pozadina_slika = models.TextField(default="nema")

    def __str__(self):
        return f"{self.ime}"

    def get_closest_race(self, target):
        return self.filter(dt__gt=target).order_by('pocetok')


class TrkaSesija(models.Model):
    trka = models.ForeignKey(Trka, on_delete=models.CASCADE)
    sesija = models.ForeignKey(Sesija, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.trka}: {self.sesija}"

# =================================================================== #

class Vest(models.Model):
    naslov = models.CharField(max_length=500)
    privju = models.CharField(max_length=1000)
    url = models.CharField(max_length=500)
    slika = models.CharField(max_length=500)
    tekst = models.TextField()
    skrejp_datum = models.DateTimeField(default=timezone.now)
    source = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.naslov

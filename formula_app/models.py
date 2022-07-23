from pyexpat import model
from django.db import models


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
    tim = models.ForeignKey(Tim, on_delete=models.CASCADE, default=get_placeholder_team)
    drzava = models.CharField(max_length=80)
    slika = models.CharField(max_length=30, default="nema-slika")

    def __str__(self):
        return f"{self.ime} {self.prezime}"
    

# =================================================================== #

class Sesija(models.Model):
    ime = models.CharField(max_length=100)
    datum = models.CharField(max_length=100)


class Trka(models.Model):
    race_id = models.IntegerField()
    status = models.CharField(max_length=20)
    ime = models.CharField(max_length=100)
    drzava = models.CharField(max_length=80)
    staza = models.CharField(max_length=100)
    pocetok = models.CharField(max_length=20)
    sesii = models.ManyToManyField(Sesija)

    def __str__(self):
        return f"{self.ime} {self.status}"

# =================================================================== #

class Vest(models.Model):
    custom_id = models.CharField(max_length=500)
    naslov = models.CharField(max_length=500)
    privju = models.CharField(max_length=1000)
    url = models.CharField(max_length=200)
    slika = models.CharField(max_length=500)
    tekst = models.TextField()
    skrejp_datum = models.DateTimeField(default = None)

    def __str__(self) -> str:
        return self.naslov

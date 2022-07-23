from bs4 import BeautifulSoup
import requests 
import json
import time
from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404
from ..models import Vest

data = []

def scrape() -> list:
    SITE_URL = "https://sport1.mk/koli-motori-i-trki"

    page = requests.get(f"{SITE_URL}")
    soup = BeautifulSoup(page.content, 'html.parser')
    blocks = soup.find_all('div', class_="col-md-4")


    for blok in blocks:
        try:
            is_formula1 = blok.find('div', class_="headline").text
            if "ФОРМУЛА" not in is_formula1:
                continue
            v_naslov = blok.find('h3', class_='title').text
            v_url = blok.find('h3', class_='title').a['href']
        except AttributeError:
            continue
        

        # ===========================================================
        # od tuka: otvara stranata na vesta 
        # zima ja slikata i celio tekst (ne samo prevjuto)

        detalna_strana = requests.get(f"https://sport1.mk{v_url}")
        detalna_supa = BeautifulSoup(detalna_strana.content, 'html.parser')
        try:
            v_slika_url = detalna_supa.find('div', class_="responsive-image").img['src']
            if v_slika_url == "unknown":
                continue
            v_privju = detalna_supa.find('div', class_='teaser').p.text
            v_teksto = "".join(x.text for x in detalna_supa.find('div', class_='content').findAll('p'))
        except AttributeError:
            continue

        # id za posle koa se prefrla so href od eden html u drug
        tid = str(int(time.time()*1000))
        v_id = f"s1-{v_naslov}-{tid}"
        skr_dat = timezone.now()

        try:
            vest = get_object_or_404(Vest, custom_id=v_id, naslov=v_naslov)
        except Http404:
            vest = Vest.objects.create(custom_id=v_id, naslov=v_naslov, skrejp_datum=skr_dat)
            vest.privju = v_privju
            vest.url = v_url
            vest.slika = v_slika_url
            vest.tekst = v_teksto

        vest.save()            
        print(vest)
        
    
    # with open('../data/vesti/telma.json', 'w') as fout:
    #     json.dump(data , fout)
        
    return data


if __name__ == '__main__':
    scrape()

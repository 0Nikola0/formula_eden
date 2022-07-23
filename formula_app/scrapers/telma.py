import imp
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
    SITE_URL = "https://telma.com.mk/kategorija/%D1%81%D0%BF%D0%BE%D1%80%D1%82/%D1%84%D0%BE%D1%80%D0%BC%D1%83%D0%BB%D0%B0-1/"
    page = requests.get(SITE_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    blocks = soup.find_all('article')

    for blok in blocks:
        try:
            v_naslov = blok.find('h2').text
            v_privju = blok.find('div', class_='entry-content').text
            v_url = blok.find('a', class_='penci-image-holder')['href']
        except AttributeError:
            continue

        # ===========================================================
        # od tuka: otvara stranata na vesta 
        # zima ja slikata i celio tekst (ne samo prevjuto)

        detalna_strana = requests.get(v_url)
        detalna_supa = BeautifulSoup(detalna_strana.content, 'html.parser')
        try:
            v_slika_url = detalna_supa.find('div', class_='post-image').img['src']
            v_teksto = "".join(detalna_supa.findAll('div', class_='entry-content')[0].text.split("©")[:-1])  #u edna linija isto so toa dole
            # teksto = teksto.split("©")[0]   # na krajo ima copyright telma zatoa e ovoa
        except AttributeError:
            continue

        # id za posle koa se prefrla so href od eden html u drug
        tid = str(int(time.time()*1000))
        v_id = f"tt-{v_naslov}-{tid}"
        skr_dat = timezone.now()
        try:
            vest = get_object_or_404(Vest, custom_id=v_id, naslov=v_naslov)
        except Http404:
            vest = Vest.objects.create(custom_id=v_id, naslov=v_naslov, skrejp_datum=skr_dat)
            vest.privju = v_privju
            vest.url = v_url
            vest.slika = v_slika_url
            vest.tekst = v_teksto

        # vest.save()            
        print(vest)
        
    
    # with open('../data/vesti/telma.json', 'w') as fout:
    #     json.dump(data , fout)
    
    return data


if __name__ == '__main__':
    scrape()

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
    SITE_URL = "https://sportski.mk/tag/%D1%84%D0%BE%D1%80%D0%BC%D1%83%D0%BB%D0%B0-1/page/"

    # (1, 4) -> 1, 2, 3
    for page_num in range(1, 3):
        page = requests.get(f"{SITE_URL}{page_num}/")
        soup = BeautifulSoup(page.content, 'html.parser')
        blocks = soup.find_all('article')

        for blok in blocks:
            try:
                v_naslov = blok.find('h2', class_='entry-title').text
                v_privju = blok.find('p', class_='block-exb').text
                v_url = blok.find('h2', class_='entry-title').a['href']
            except AttributeError:
                continue
            
            # print(f"{v_naslov}\n {v_privju} \n {v_url}\n\n=====\n")

            # ===========================================================
            # od tuka: otvara stranata na vesta 
            # zima ja slikata i celio tekst (ne samo prevjuto)

            detalna_strana = requests.get(v_url)
            detalna_supa = BeautifulSoup(detalna_strana.content, 'html.parser')
            try:
                v_slika_url = detalna_supa.find('img', class_='attachment-bdaia-large')['src']
                if v_slika_url == "unknown":
                    continue
                v_teksto = "".join(x.text for x in detalna_supa.find('div', class_='bdaia-post-content').findAll('p'))
            except AttributeError:
                continue

            # id za posle koa se prefrla so href od eden html u drug
            tid = str(int(time.time()*1000))
            v_id = f"smk-{v_naslov}-{tid}"
            skr_dat = timezone.now()

            try:
                vest = get_object_or_404(Vest, custom_id=v_id, naslov=v_naslov)
            except Http404:
                vest = Vest.objects.create(custom_id=v_id, naslov=v_naslov, skrejp_datum=skr_dat)
                vest.privju = v_privju
                vest.url = v_url
                vest.slika = v_slika_url
                vest.tekst = v_teksto
                # vest.skrejp_datum = datetime.datetime.now()

            vest.save()            
            print(vest)
            
        
        # with open('../data/vesti/telma.json', 'w') as fout:
        #     json.dump(data , fout)
        
    return data


if __name__ == '__main__':
    scrape()

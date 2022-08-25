import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from django.http import Http404
from django.shortcuts import get_object_or_404
from ..models import Vest


def scrape() -> str:
    message = "Vesti: {\n"

    SITE_URL = "https://sport1.mk/koli-motori-i-trki"
    ua = UserAgent()

    page = requests.get(f"{SITE_URL}", headers={'User-Agent': ua.chrome})
    soup = BeautifulSoup(page.content, 'html.parser')
    blocks = soup.find_all('div', class_="col-md-4")

    for blok in blocks:
        try:
            is_formula1 = blok.find('div', class_="headline").text
            if "ФОРМУЛА" not in is_formula1:
                continue
            v_naslov = blok.find('h3', class_='title').text.strip()
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

        try:
            vest = get_object_or_404(Vest, naslov=v_naslov)
        except Http404:
            vest = Vest.objects.create(naslov=v_naslov)
            vest.privju = v_privju
            vest.url = v_url
            vest.slika = v_slika_url
            vest.tekst = v_teksto
            vest.source = "sport1.mk"
            message += f"\t\"{v_naslov}\",\n"

        vest.save()

    message += "}"

    return message


if __name__ == '__main__':
    scrape()

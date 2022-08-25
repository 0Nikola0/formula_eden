import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from django.http import Http404
from django.shortcuts import get_object_or_404
from ..models import Vest


def scrape() -> str:
    message = "Vesti: {\n"
    
    SITE_URL = "https://telma.com.mk/kategorija/%D1%81%D0%BF%D0%BE%D1%80%D1%82/%D1%84%D0%BE%D1%80%D0%BC%D1%83%D0%BB%D0%B0-1/"
    ua = UserAgent()

    page = requests.get(SITE_URL, headers={'User-Agent': ua.chrome})
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

        try:
            vest = get_object_or_404(Vest, naslov=v_naslov)
        except Http404:
            vest = Vest.objects.create(naslov=v_naslov)
            vest.privju = v_privju
            vest.url = v_url
            vest.slika = v_slika_url
            vest.tekst = v_teksto
            vest.source = "telma.mk"
            message += f"\t\"{v_naslov}\"\n"

        vest.save()
    
    message += "}"
    return message


if __name__ == '__main__':
    scrape()

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from django.http import Http404
from django.shortcuts import get_object_or_404
from ..models import Vest


def scrape() -> str:
    vesti = []
    message = "Vesti: {\n"
    
    SITE_URL = "https://sportski.mk/tag/%D1%84%D0%BE%D1%80%D0%BC%D1%83%D0%BB%D0%B0-1/"
    ua = UserAgent()

    page = requests.get(SITE_URL, headers={'User-Agent': ua.chrome})
    soup = BeautifulSoup(page.content, 'html.parser')
    blocks = soup.find_all('article')

    for blok in blocks:
        try:
            v_naslov = blok.find('h2', class_='entry-title').text
            v_privju = blok.find('p', class_='block-exb').text
            v_url = blok.find('h2', class_='entry-title').a['href']
        except AttributeError:
            continue
        
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

        vesti.append({
            "v_naslov": v_naslov,
            "v_privju": v_privju,
            "v_url": v_url,
            "v_slika_url": v_slika_url,
            "v_teksto": v_teksto,
        })

    # Scrape prae od najnova do najstara i ako ne napraam reverse [::-1] na stranata ne gi pokazuva po ubav redosled
    for v in vesti[::-1]:
        try:
            vest = get_object_or_404(Vest, naslov=v["v_naslov"])
        except Http404:
            vest = Vest.objects.create(naslov=v["v_naslov"])
            vest.privju = v["v_privju"]
            vest.url = v["v_url"]
            vest.slika = v["v_slika_url"]
            vest.tekst = v["v_teksto"]
            vest.source = "sportski.mk"
            message += f"\t\"{v['v_naslov']}\",\n"

        vest.save()
    
    message += "}"
    return message


if __name__ == '__main__':
    scrape()

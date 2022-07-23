from bs4 import BeautifulSoup
import requests 
import json
import time

data = []

def scrape() -> list:
    print("""
    NE RABOTE VEKJE OVOA
    (do niv e nisto nema na stranata vesti za f1)
    """)
    SITE_URL = "https://24.mk/formula-1"
    page = requests.get(SITE_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    blocks = soup.find_all('div', class_='item')

    for blok in blocks:
        try:
            naslov = blok.find('div', class_='title-left').text.strip()
            privju = blok.find('p').text.split("\n")[0].strip()
            url = 'https://24.mk' + blok.find('a')['href']
        except AttributeError:
            continue
        
        # ===========================================================
        # od tuka: otvara stranata na vesta 
        # zima ja slikata i celio tekst (ne samo prevjuto)

        detalna_strana = requests.get(url)
        detalna_supa = BeautifulSoup(detalna_strana.content, 'html.parser')
        
        try:
            slika_url = detalna_supa.find('div', class_='entry-media').img['src']
            teksto = detalna_supa.findAll('div', class_='entry-content')[0].text.strip()
        except AttributeError:
            continue

        # id za posle koa se prefrla so href od eden html u drug
        tid = str(int(time.time()*1000))
        id = f"dc-{naslov}-{tid}"
        data.append(
            {
                'id': id,
                'naslov': naslov,
                'privju': privju,
                'url': url,
                'slika': slika_url,
                'tekst': teksto
            }
        )
        
    with open('../data/vesti/dvaes-cetiri.json', 'w') as fout:
        json.dump(data , fout)
    
    return data


if __name__ == '__main__':
    scrape()

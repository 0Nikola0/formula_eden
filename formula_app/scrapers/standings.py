# TODO mos ke e podobro sekoja funkc u poseben file za preglednosr
import json
import requests
import datetime
from dotenv import load_dotenv
import os
from ..models import Vozac, Tim, Trka, Sesija
from django.utils import timezone
from django.utils.dateparse import parse_date

'''
    Prvite 3 API se 1000 request sekoj mesec
    poslednoto e 250 mesec, 60 u minuta
'''

load_dotenv()
ST_API_KEY = os.getenv("ST_API_KEY")
MR_API_KEY = os.getenv("MR_API_KEY")

def get_driver_standings():
    message = "Starting update\n\n"
    url = "https://formula-1-standings.p.rapidapi.com/standings/drivers"
    headers = {
        "X-RapidAPI-Key": ST_API_KEY,
        "X-RapidAPI-Host": "formula-1-standings.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    message += f"Response code: {response.status_code}\n\n"
    data = list(response.json()['results'])
    message += f"Data: {json.dumps(data, indent=4)}\n\n"
    # with open('../data/plasman/vozaci-plasman.json', 'w') as fout:
    #     json.dump(data , fout)
    for i, j in enumerate(data):
        v_ime, v_prezime = j['driver_name'].split(" ")
        v_pozicija = int(j['position'] )
        v_poeni = int(j['points'])
        v_tim = Tim.objects.get(ime=j['team_name'])
        v_drzava = j['nationality']

        vozac = Vozac.objects.get_or_create(ime=v_ime, prezime=v_prezime, drzava=v_drzava)[0]
        vozac.pozicija=v_pozicija
        vozac.poeni=v_poeni
        vozac.tim=v_tim
        vozac.slika = f"formula_app/imgs/drivers/{v_prezime}.png"

        print(vozac)
        vozac.save()

    message += "Successfullly updated\n\n"
    
    return message


def get_constructor_standings():
    message = "Starting update\n\n"
    url = "https://formula-1-standings.p.rapidapi.com/standings/constructors"
    headers = {
        "X-RapidAPI-Key": ST_API_KEY,
        "X-RapidAPI-Host": "formula-1-standings.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    message += f"Response code: {response.status_code}\n\n"
    data = list(response.json()['results'])
    message += f"Data: {json.dumps(data, indent=4)}\n\n"
    # with open('../data/plasman/timovi-plasman.json', 'w') as fout:
    #     json.dump(data , fout)

    for i, j in enumerate(data):
        t_poeni = int(j['points'])
        t_ime = j['team_name']

        tim = Tim.objects.get_or_create(ime=t_ime)[0]
        tim.pozicija=j['position']
        tim.poeni=t_poeni

        print(tim)
        tim.save()

    message += "Successfullly updated\n\n"
    return message


def get_simple_races():
    print(
        """
        DEPRECATED FUNCTION
        function: get_simple_races()
        trace: formula_app/scrapers/standings.py/get_simple_races()
        """
    )
    return None
    '''
        Vrakja prazen response, koristi go drugio api od ozdole
        - ok e sea vrakja ama ima pomalku info
         samo koga e trkata (nema fp1 fp2 quali...)
    '''
    url = "https://formula-1-standings.p.rapidapi.com/races"
    headers = {
        "X-RapidAPI-Key": ST_API_KEY,
        "X-RapidAPI-Host": "formula-1-standings.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    with open('simple-trki.json', 'w') as fout:
        json.dump(data, fout)
    return data


def get_races():
    '''
        250 request sekoj mesec
        60 requests u minuta
    '''
    message = "Starting update\n\n"
    url = "https://f1-live-motorsport-data.p.rapidapi.com/races/2022"
    headers = {
	"X-RapidAPI-Key": MR_API_KEY,
	"X-RapidAPI-Host": "f1-live-motorsport-data.p.rapidapi.com"
}
    response = requests.request("GET", url, headers=headers)
    message += f"Response code: {response.status_code}\n\n"
    data = list(response.json()['results'])
    message += f"Data: {json.dumps(data, indent=4)}\n\n"
    # with open('../data/trki/trki.json', 'w') as fout:
    #     json.dump(data, fout)

    for i, j in enumerate(data):
        t_id = int(j['race_id'])
        t_status = j['status']
        t_ime = j['name']
        t_drzava = j['country']
        t_staza = j['track']
        y,m,d = [int(i) for i in j['start_date'].split("-")]
        t_pocetok = datetime.date(y, m, d)
        y,m,d = [int(i) for i in j['end_date'].split("-")]
        t_kraj = datetime.date(y, m, d)
        sesii = list()

        for sesija in j['sessions']:
            s_ime = sesija['session_name']
            s_datum = sesija['date']
            model_sesija = Sesija.objects.get_or_create(session_id=sesija['id'])[0]
            model_sesija.ime = s_ime
            model_sesija.trka_ime = t_ime
            model_sesija.datum = timezone.datetime.fromisoformat(s_datum)
            model_sesija.save()
            sesii.append(model_sesija)
        
        trka = Trka.objects.get_or_create(race_id=t_id, ime=t_ime, drzava=t_drzava, staza=t_staza)[0]
        trka.sesii.set(sesii)
        trka.status = t_status
        trka.pocetok = t_pocetok
        trka.kraj = t_kraj
        trka.staza_slika = f'formula_app/imgs/tracks/{t_ime.replace(" ","-")}.png'
        trka.pozadina_slika = f'formula_app/imgs/track-Backgrounds/{t_ime.replace(" ","-")}.jpg'
        
        # print(trka)
        trka.save()
        
    message += "Successfullly updated\n\n"
    return data


if __name__ == '__main__':
    # get_driver_standings()
    get_constructor_standings()
    # get_races()
import json

wlasciwosci = {
    ############## wojownicy
    "bloker": {
        "typ" : "plansza",
        "liczbajednostek" : 2,
        "hp": 3,
        "pancerz": [0]
    },
    "hybryda": {
        "typ" : "plansza",
        "liczbajednostek" : 2,
        "hp": 1,
        "ataki" : {
            "shoot": [[0, 1]],
        },
        "inicjatywa": [3]
    },
    "dzialkogaussa": {
        "typ" : "plansza",
        "liczbajednostek" : 1,
        "hp": 2,
        "ataki" : {
            "gauss": [[4, 1]],
        },
        "inicjatywa": [1]
    },
    "juggernaut": {
        "typ" : "plansza",
        "liczbajednostek" : 1,
        "hp": 2,
        "ataki" : {
            "shoot" : [[1, 1]],
            "melee": [[0, 2]],
        },
        "pancerz": [0, 2, 4],
        "inicjatywa": [1]
    },
    "klaun": {
        "typ" : "plansza",
        "liczbajednostek" : 1,
        "hp": 2,
        "ataki" : {
            "melee": [[0, 1], [5, 1]],
        },
        "inicjatywa": [2]
    },
    "lowca": {
        "typ" : "plansza",
        "liczbajednostek" : 2,
        "hp": 1,
        "ataki" : {
            "melee": [[0, 1], [1, 1], [3, 1], [5, 1]],
        },
        "inicjatywa": [3]
    },
    "obronca": {
        "typ" : "plansza",
        "liczbajednostek" : 1,
        "hp": 2,
        "ataki" : {
            "shoot": [[0, 1], [1, 1], [5, 1]],
        },
        "inicjatywa": [1]
    },
    "opancerzonylowca": {
        "typ" : "plansza",
        "liczbajednostek" : 2,
        "hp": 2,
        "ataki" : {
            "melee": [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
        },
        "pancerz": [0, 5],
        "inicjatywa": [2]
    },
    "opancerzonywartownik": {
        "typ" : "plansza",
        "liczbajednostek" : 1,
        "hp": 1,
        "ataki" : {
            "shoot": [[0, 1], [5, 1]],
        },
        "inicjatywa": [2]
    },
    "szerszeń": {
        "typ" : "plansza",
        "liczbajednostek" : 1,
        "hp": 1,
        "ataki" : {
            "melee": [[0, 2]],
        },
        "inicjatywa": [2]
    },
    "sieciarz": {
        "typ" : "plansza",
        "liczbajednostek" : 1,
        "hp": 1,
        "siec": [0, 5]
    },
    "sztab": {
        "typ" : "plansza",
        "liczbajednostek" : 1,
        "hp": 20,
        "wzmocniony_atak": [0, 1, 2, 3, 4, 5],
        "ataki" : {
            "melee": [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
        },
        "inicjatywa": [0]
    },
    "szturmowiec": {
        "typ" : "plansza",
        "liczbajednostek" : 1,
        "hp": 2,
        "ataki" : {
            "shoot": [[0, 1]],
        },
        "inicjatywa": [1, 2]
    },
    "wartownik": {
        "typ" : "plansza",
        "liczbajednostek" : 1,
        "hp": 1,
        "pancerz": [0],
        "ataki" : {
            "shoot": [[1, 1], [5, 1]],
        },
        "inicjatywa": [2]
    },

    ############## moduły
    "oficer": {
        "typ" : "plansza",
        "liczbajednostek" : 1,
        "hp": 1,
        "wzmocniony_strzal": [1, 3, 5]
    },
    "zwiadowca": {
        "typ" : "plansza",
        "liczbajednostek" : 1,
        "hp": 1,
        "wyzsza_inicjatywa": [0, 2, 4]
    },
    "matka": {
        "typ" : "plansza",
        "liczbajednostek" : 1,
        "hp": 1,
        "dodatkowa_inicjatywa": [0]
    },
    "medyk": {
        "typ" : "plansza",
        "liczbajednostek" : 2,
        "hp": 1,
        "leczenie": [0, 2, 4]
    },
    "mozg": {
        "typ" : "plansza",
        "liczbajednostek" : 1,
        "hp": 1,
        "wzmocniony_strzal": [0, 2, 4],
        "wzmocniony_atak": [0, 2, 4]
    },
    ############# natychmiastowe
    "bitwa": {
        "typ" : "natychmiastowy",
        "liczbajednostek" : 4,
    },
    "ruch": {
        "typ" : "natychmiastowy",
        "liczbajednostek" : 1,
    },
    "odepchniecie": {
        "typ" : "natychmiastowy",
        "liczbajednostek" : 5,
    },
    "bomba": {
        "typ" : "natychmiastowy",
        "liczbajednostek" : 1,
    }
}
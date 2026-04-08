import json

wlasciwosci = {
    ############## wojownicy
    "mutek": {
        "typ": "plansza",
        "liczbajednostek": 6,
        "hp": 1,
        "ataki": {
            "melee": [[0, 1], [1, 1], [5, 1]],
        },
        "inicjatywa": [2]
    },
    "nożownik": {
        "typ": "plansza",
        "liczbajednostek": 4,
        "hp": 1,
        "ataki": {
            "melee": [[4, 1], [5, 1]],
        },
        "inicjatywa": [3]
    },
    "sieciarz": {
        "typ": "plansza",
        "liczbajednostek": 2,
        "hp": 1,
        "ataki": {
            "melee": [[2, 3]],
        },
        "siec" : [2],
        "inicjatywa": [1]
    },
    "super-mutant": {
        "typ": "plansza",
        "liczbajednostek": 1,
        "hp": 2,
        "ataki": {
            "melee": [[0, 2], [1, 2], [5, 1]],
        },
        "pancerz" : [0, 1, 5],
        "inicjatywa": [2]
    },
    "siłacz": {
        "typ": "plansza",
        "liczbajednostek": 2,
        "hp": 1,
        "ataki": {
            "melee": [[0, 2]],
        },
        "inicjatywa": [2]
    },
    "zabójca": {
        "typ": "plansza",
        "liczbajednostek": 2,
        "hp": 1,
        "ataki": {
            "shoot": [[5, 1]],
        },
        "abilitki" : ["mobilność"],
        "inicjatywa": [3]
    },
    ############## sztab
    "sztab": {
        "typ": "plansza",
        "liczbajednostek": 1,
        "hp": 20,
        "ataki": {
            "melee": [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
        },
        "wyzsza_inicjatywa": [0, 1, 2, 3, 4, 5],
        "inicjatywa": [0]
    },

    ############## moduły
    "medyk": {
        "typ": "plansza",
        "liczbajednostek": 1,
        "hp": 1,
        "leczenie": [0, 1, 5]
    },
    "oficer": {
        "typ": "plansza",
        "liczbajednostek": 2,
        "hp": 1,
        "wzmocniony_atak": [0, 1, 5]
    },
    "super-oficer": {
        "typ": "plansza",
        "liczbajednostek": 1,
        "hp": 2,
        "wzmocniony_atak": [0, 1, 5]
    },
    "zwiadowca": {
        "typ": "plansza",
        "liczbajednostek": 2,
        "hp": 1,
        "wyzsza_inicjatywa": [0, 1, 5]
    },

    ############# natychmiastowe
    "bitwa": {
        "typ": "natychmiastowy",
        "liczbajednostek": 6,
    },
    "ruch": {
        "typ": "natychmiastowy",
        "liczbajednostek": 4,
    },
    "granat": {
        "typ": "natychmiastowy",
        "liczbajednostek": 1,
    }
}
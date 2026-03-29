import json

wlasciwosci = {
    "bloker": {
        "liczbajednostek" : 2,
        "hp": 3,
        "pancerz": [0]},
    "hybryda": {
        "liczbajednostek" : 2,
        "hp": 1,
        "strzal": [[0, 1]],
        "inicjatywa": [3]},
    "dzialkogaussa": {
        "liczbajednostek" : 1,
        "hp": 2,
        "gauss": [[5, 1]],
        "inicjatywa": [1]},
    "juggernaut": {
        "liczbajednostek" : 1,
        "hp": 2,
        "strzal" : [[2, 1]],
        "pancerz": [0, 2, 4],
        "atak": [[0, 2]],
        "inicjatywa": [1]},
    "klaun": {
        "liczbajednostek" : 1,
        "hp": 2,
        "atak": [[0, 1], [5, 1]],
        "inicjatywa": [2]},
    "lowca": {
        "liczbajednostek" : 2,
        "hp": 1,
        "atak": [[0, 1], [1, 1], [3, 1], [5, 1]],
        "inicjatywa": [3]},
    "obronca": {
        "liczbajednostek" : 1,
        "hp": 2,
        "strzal": [[0, 1], [1, 1], [5, 1]],
        "inicjatywa": [1]},
    "opancerzonylowca": {
        "liczbajednostek" : 2,
        "hp": 2,
        "atak": [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
        "pancerz": [0, 5],
        "inicjatywa": [2]},
    "opancerzonywartownik": {
        "liczbajednostek" : 1,
        "hp": 1,
        "strzal": [[0, 1], [5, 1]],
        "inicjatywa": [2]},
    "szerszeń": {
        "liczbajednostek" : 1,
        "hp": 1,
        "atak": [[0, 2]],
        "inicjatywa": [2]},
    "sieciarz": {
        "liczbajednostek" : 1,
        "hp": 1,
        "siec": [0, 5]},
    "sztab": {
        "liczbajednostek" : 1,
        "hp": 20,
        "wzmocniony_atak": [0, 1, 2, 3, 4, 5],
        "atak": [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
        "inicjatywa": [0]},
    "szturmowiec": {
        "liczbajednostek" : 1,
        "hp": 2,
        "strzal": [[0, 1]],
        "inicjatywa": [1, 2]},
    "wartownik": {
        "liczbajednostek" : 1,
        "hp": 1,
        "pancerz": [0],
        "atak": [[0, 1], [5, 1]],
        "inicjatywa": [2]},
    # "oficer": {
    #     "liczbajednostek" : 1,
    #     "hp": 1,
    #     "wzmocniony_strzal": [1, 3, 5]},
    # "zwiadowca": {
    #     "liczbajednostek" : 1,
    #     "hp": 1,
    #     "wyzsza_inicjatywa": [0, 2, 4]},
    # "matka": {
    #     "liczbajednostek" : 1,
    #     "hp": 1,
    #     "dodatkowa_inicjatywa": [0]},
    # "medyk": {
    #     "liczbajednostek" : 2,
    #     "hp": 1,
    #     "leczenie": [0, 2, 4]},
    # "mozg": {
    #     "liczbajednostek" : 1,
    #     "hp": 1,
    #     "wzmocniony_strzal": [0, 2, 4],
    #     "wzmocniony_atak": [0, 2, 4]},
}
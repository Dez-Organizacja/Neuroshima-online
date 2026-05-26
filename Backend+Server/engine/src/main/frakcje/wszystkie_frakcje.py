from importlib import import_module
from copy import deepcopy
# import main.frakcje.moloch

dostepne_frakcje = ["moloch", "borgo", "testowa"]
path = "main.frakcje"
frakcje : dict[str, dict] = {}

for frakcja in dostepne_frakcje:
    lib = import_module(f"{path}.{frakcja}")
    frakcje[frakcja] = deepcopy(lib.wlasciwosci)
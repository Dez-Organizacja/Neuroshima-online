import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from variable import Token
from variable import Attack

wlasciwosci = {
    ############## wojownicy
    "bloker": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 2,
        Token.Stats.HP: 3,
        Token.Stats.ARMOR: [0]
    },
    "hybryda": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 2,
        Token.Stats.HP: 1,
        Token.Stats.ATTACKS : {
            Attack.SHOOT: [[0, 1]],
        },
        Token.Stats.INITIATIVE: [3]
    },
    "dzialkogaussa": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 1,
        Token.Stats.HP: 2,
        Token.Stats.ATTACKS : {
            Attack.GAUSS: [[4, 1]],
        },
        Token.Stats.INITIATIVE: [1]
    },
    "juggernaut": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 1,
        Token.Stats.HP: 2,
        Token.Stats.ATTACKS : {
            Attack.SHOOT : [[1, 1]],
            Attack.MELEE: [[0, 2]],
        },
        Token.Stats.ARMOR: [0, 2, 4],
        Token.Stats.INITIATIVE: [1]
    },
    "klaun": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 1,
        Token.Stats.HP: 2,
        Token.Stats.ATTACKS : {
            Attack.MELEE: [[0, 1], [5, 1]],
        },
        Token.Stats.INITIATIVE: [2]
    },
    "lowca": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 2,
        Token.Stats.HP: 1,
        Token.Stats.ATTACKS : {
            Attack.MELEE: [[0, 1], [1, 1], [3, 1], [5, 1]],
        },
        Token.Stats.INITIATIVE: [3]
    },
    "obronca": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 1,
        Token.Stats.HP: 2,
        Token.Stats.ATTACKS : {
            Attack.SHOOT: [[0, 1], [1, 1], [5, 1]],
        },
        Token.Stats.INITIATIVE: [1]
    },
    "opancerzonylowca": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 2,
        Token.Stats.HP: 2,
        Token.Stats.ATTACKS : {
            Attack.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
        },
        Token.Stats.ARMOR: [0, 5],
        Token.Stats.INITIATIVE: [2]
    },
    "opancerzonywartownik": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 1,
        Token.Stats.HP: 1,
        Token.Stats.ATTACKS : {
            Attack.SHOOT: [[0, 1], [5, 1]],
        },
        Token.Stats.INITIATIVE: [2]
    },
    "szerszeń": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 1,
        Token.Stats.HP: 1,
        Token.Stats.ATTACKS : {
            Attack.MELEE: [[0, 2]],
        },
        Token.Stats.INITIATIVE: [2]
    },
    "sieciarz": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 1,
        Token.Stats.HP: 1,
        Token.Stats.WIRE: [0, 5]
    },
    "sztab": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 1,
        Token.Stats.HP: 20,
        "wzmocniony_atak": [0, 1, 2, 3, 4, 5],
        Token.Stats.ATTACKS : {
            Attack.MELEE: [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1]],
        },
        Token.Stats.INITIATIVE: [0]
    },
    "szturmowiec": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 1,
        Token.Stats.HP: 2,
        Token.Stats.ATTACKS : {
            Attack.SHOOT: [[0, 1]],
        },
        Token.Stats.INITIATIVE: [1, 2]
    },
    "wartownik": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 1,
        Token.Stats.HP: 1,
        Token.Stats.ARMOR: [0],
        Token.Stats.ATTACKS : {
            Attack.SHOOT: [[1, 1], [5, 1]],
        },
        Token.Stats.INITIATIVE: [2]
    },

    ############## moduły
    "oficer": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 1,
        Token.Stats.HP: 1,
        "wzmocnienia":{
            "wzmocniony_strzal": [1, 3, 5]
        }
    },
    "zwiadowca": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 1,
        Token.Stats.HP: 1,
        "wzmocnienia":{
            "wyzsza_inicjatywa": [0, 2, 4]
        }
    },
    "matka": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 1,
        Token.Stats.HP: 1,
        "wzmocnienia":{
            "dodatkowa_inicjatywa": [0]
        }
    },
    "medyk": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 2,
        Token.Stats.HP: 1,
        "wzmocnienia":{
            "leczenie": [0, 2, 4]
        }
    },
    "mozg": {
        Token.TYPE : Token.Type.BOARD,
        Token.UNIT_COUNT : 1,
        Token.Stats.HP: 1,
        "wzmocnienia":{
            "wzmocniony_strzal": [0, 2, 4],
            "wzmocniony_atak": [0, 2, 4]
        }
    },
    ############# natychmiastowe
    "bitwa": {
        Token.TYPE : Token.Type.INSTANT,
        Token.UNIT_COUNT : 4,
    },
    "ruch": {
        Token.TYPE : Token.Type.INSTANT,
        Token.UNIT_COUNT : 1,
    },
    "odepchniecie": {
        Token.TYPE : Token.Type.INSTANT,
        Token.UNIT_COUNT : 5,
    },
    "bomba": {
        Token.TYPE : Token.Type.INSTANT,
        Token.UNIT_COUNT : 1,
    }
}
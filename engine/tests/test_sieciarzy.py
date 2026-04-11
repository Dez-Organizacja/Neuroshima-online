import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from collections import defaultdict
from plansza import Board

# from plansza import Board

def print_printy(board):
    print("Plansza:")
    board.print_board()

    print("\nTestowanie kwestii sieciarzy...")
    board.kwestia_sieciarzy()

    print("\nGraf sieciarzy:")
    for k, v in board.graf_sieciarzy.items():
        print(f"{k} -> {v}")

    print("\nOdwrócony graf:")
    for k, v in board.odwr_sieciarzy.items():
        print(f"{k} -> {v}")

    print("\nKolory SCC:")
    for siec, kolor in board.kolory.items():
        print(f"{siec} -> kolor {kolor}")

    print("\nSieciarze w kolorach:")
    for kolor, sieci in board.sieci_w_kolorze.items():
        print(f"Kolor {kolor}: {sieci}")

    print("\nGraf między SCC:")
    for k, v in board.graf_scc.items():
        print(f"SCC {k} -> {v}")

    print("----------------------------------\n")


def test_scc():
    board = Board()

    # [0, 5]
    board.postaw_zeton(2, 4, { 
        "frakcja": "moloch",
        "nazwa": "sieciarz",
        "rotacja": 1,
        "rany": 0
    })

    board.postaw_zeton(0, 4, { 
        "frakcja": "moloch",
        "nazwa": "sieciarz",
        "rotacja": 3,
        "rany": 0
    })

    # [0]
    board.postaw_zeton(1, 3, {
        "frakcja": "testowa",
        "nazwa": "sieciarz",
        "rotacja": 2,
        "rany": 0
    })

    board.postaw_zeton(2, 6, {
        "frakcja": "testowa",
        "nazwa": "sieciarz",
        "rotacja": 0,
        "rany": 0
    })

    board.postaw_zeton(1, 5, {
        "frakcja": "testowa",
        "nazwa": "sieciarz",
        "rotacja": 5,
        "rany": 0
    })

    pop = defaultdict(int, {(2, 4): 1, (0, 4): 1, (1, 5): 1, (1, 3): 1, (2, 6): 2})
    
    board.kwestia_sieciarzy()
    data = board.sieciarze.status_sieciarzy

    # print(data)
    # print(data == pop)
    # print_printy(board)

    assert (data == pop)

    board.postaw_zeton(1, 1, { 
        "frakcja": "moloch",
        "nazwa": "sieciarz",
        "rotacja": 1,
        "rany": 0
    })

    pop = defaultdict(int, {(1, 1): 1, (2, 4): 1, (0, 4): 1, (1, 5): 2, (1, 3): 2, (2, 6): 2})
    
    board.kwestia_sieciarzy()
    data = board.sieciarze.status_sieciarzy

    # print(data)
    # print(data == pop)
    # print_printy(board)

    assert (data == pop)

if __name__ == "__main__":
    test_scc()
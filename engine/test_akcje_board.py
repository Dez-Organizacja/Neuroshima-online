import pytest
from akcje import Actions
from main import Game
from plansza import Board

class DummyGame:
    def __init__(self):
        self.bottoms = ["koniec tury", "kosz", "użyj", "cancel", "tak", "nie"]

class Test_board:


    def test_start(self):
        data = {
            "faza": "newgame",
            "frakcje": {
                "player1": "borgo",
                "player2": "moloch"
            }
        }

        game = Game(data)
        self.output = game.export_game_state()
        # print(self.output)

        poprawne = {}
        poprawne["faza"] = "sztaby"
        poprawne["next_turns"] = [{"frakcja" : "borgo", "typ" : "wystaw_sztab"}, {"frakcja" : "moloch", "typ" : "wystaw_sztab"}, {'frakcja': 'bitwa', 'typ': 'ostatnia'}]
        poprawne["current_frakcja"] = "borgo"
        poprawne["user_actions"] = []
        poprawne["board"] = [[None for _ in range(9)] for _ in range(5)]
        # trzeba nanosic kazda zmiane, bo moga zmieniac poprawne z zmiana koncepji
        assert (self.output["board"] == poprawne["board"])
        assert (self.output["current_frakcja"] == "borgo")


    def run_wstawianie(self, board, action, nazwa, frakcja, expected):
        akcje = Actions(DummyGame())
        hand = [nazwa, "a", "b"]
        previous_board = [[board.get_type(x, y) for y in range(board.length)] for x in range(board.width)]
        # print("Previous board:")
        # for row in previous_board:
        #     print(row)

        status = akcje.wstawianie(board, hand, action, nazwa, frakcja)

        assert (status == expected)

        if(status):
            ax = action["x"]
            ay = action["y"]
            assert (board.get_type(ax, ay) == frakcja)
            zeton = board.board[ax][ay]
            assert (zeton.nazwa == nazwa)
            assert (zeton.frakcja == frakcja)
            assert (zeton.rany == 0)
            assert (zeton.rotacja == 0)
            for x in range(board.width):
                for y in range(board.length):
                    if(x == ax and y == ay):
                        continue
                    assert (board.get_type(x, y) == previous_board[x][y])
        
        else:
            for x in range(board.width):
                for y in range(board.length):
                    assert (board.get_type(x, y) == previous_board[x][y])
                    
        return status

    # def test_wstawianie(self):
    #     board = Board()
    #     frakcja = "moloch"
    #     nazwa = "sieciarz"
    #     action = {"x": 1, "y": 7}
    #     assert(self.run_wstawianie(board, action, nazwa, frakcja, True) == True)
        
    #     nazwa = "klaun"
    #     action = {"x": 5, "y": 7}
    #     assert(self.run_wstawianie(board, action, nazwa, frakcja, False) == False)

    #     action = {"x": 1, "y": 7}
    #     assert(self.run_wstawianie(board, action, nazwa, frakcja, False) == False)
    
    #     frakcja = "borgo"
    #     nazwa = "mutek"
    #     action = {"x": 2, "y": 2}
    #     assert(self.run_wstawianie(board, action, nazwa, frakcja, True) == True)

    #     frakcja = "moloch"
    #     nazwa = "bloker"
    #     action = {"x": 2, "y": 2}
    #     assert(self.run_wstawianie(board, action, nazwa, frakcja, False) == False)
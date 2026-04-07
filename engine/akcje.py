from copy import deepcopy

class Actions:
    def __init__(self, game):
        self.MAX_HAND_SIZE = 3
        self.available_structure = {
            "hand" : False,
            "bottoms" : {bottom : False for bottom in game.bottoms}
        }
        self.handlers = {
            "hand" : self.handle_hand,
            "rotate" : self.handle_rotate,
            "done" : self.handle_done,
        }

    #############################################################################
    #   Board functions       
    #############################################################################
    def wstawianie(self, board, hand, action, nazwa, frakcja):
        # print("Wstawianie:", action, nazwa, frakcja)
        x = action["x"]
        y = action["y"]

        # print("ok")
        if(not board.on_board(x, y)):
            return False

        if(not board.is_empty(x, y)):
            return False
        
        self.odrzuc(hand, nazwa)
        zeton = {"nazwa" : nazwa, "frakcja" : frakcja, "rany" : 0, "rotacja" : 0}
        board.postaw_zeton(x, y, zeton)
        # self.print_board(board)
        board.update_available_hexs({"x" : x, "y" : y})
        return True

    #############################################################################
    #   Hand functions       
    #############################################################################
    def resize_hand(self, hand):
        while(len(hand) > 0 and hand[-1] is None):
            hand.pop(-1)

    def fill_hand(self, hand):
        while(len(hand) < self.MAX_HAND_SIZE):
            hand.append(None)

    def dobierz(self, hand, pile, nazwa):
        hand.append(nazwa)
        pile.remove(nazwa)

    def odrzuc(self, hand, zeton):
        hand.remove(zeton)

    def dociag(self, hand, pile):
        while(len(hand) < self.MAX_HAND_SIZE and len(pile) > 0):
                self.dobierz(hand, pile, pile[-1])

    def get_from_hand(self, hand, click):
        if(not isinstance(click, int)):
            return None

        if(len(hand) <= click):
            return None

        return hand[click]



    def from_hand(self, game, action, zeton):
        hand = game.hand[game.current_frakcja]
        if(zeton is None):
            return False

        if(action["type"] == "board"):
            status = self.wstawianie(game.board, hand, action, zeton, game.current_frakcja)
            if(status):
                game.user_actions.clear()
                self.update_available_actions(game, deepcopy(self.available_structure))
                return None
            return status

        elif(action["type"] == "odrzuc"):
            self.odrzuc(hand, zeton)
            return True
        
        elif(action["type"] == "cancel"):
            return True

        else:
            return False

    def hand_available_actions(self, game):
        available = deepcopy(self.available_structure)

        game.board.update_available_hexs(None)

        available["bottoms"]["cancel"] = True
        if(game.faza != "sztaby"):
            available["bottoms"]["kosz"] = True
        self.update_available_actions(game, available)
    #############################################################################
    #   Turn functions       
    #############################################################################
    def poczatek_tury(self, game):
        if(game.current_frakcja != None):
            return False
        frakcja = game.next_turns[0]["frakcja"]
        typ = game.next_turns[0]["typ"]
        
        # if(frakcja == "bitwa"):
        #     bitwa()
        #     return

        game.current_frakcja = frakcja
        if(typ == "wystaw_sztab"):
            game.faza = "sztaby"
            self.dobierz(game.hand[frakcja], game.pile[frakcja], "sztab")

        else:
            game.faza = "tura"
            self.dociag(game.hand[frakcja], game.pile[frakcja])

        if(len(game.pile[frakcja]) == 0):
            game.next_turns.append({"frakcja" : "bitwa", "typ" : "ostatnia"})

        return True

    def koniec_tury(self, game, check=False):

        next_turn = game.next_turns[0]
        frakcja = next_turn["frakcja"]
        typ = next_turn["typ"]

        if((typ == "wystaw_sztab") and (len(game.hand[frakcja]) > 0)):
            return False
        
        # if(frakcja == "bitwa"):
        #     return True
        
        if(len(game.hand[frakcja]) == 3):
            return False
        
        if(check):
            return True
        
        game.next_turns.pop(0)
        game.next_turns.append({"frakcja" : frakcja, "typ" : "tura"})
        game.current_frakcja = None
        return True

    #############################################################################
    #   General functions       
    #############################################################################
    def invalid_move(self, user_actions):
        print("INVALID MOVE")
        user_actions.clear()
    
    def get_first(self, actions):
        if(actions is None or len(actions) == 0):
            return None
        
        return actions.pop(0)
    
    def print_board(self, board):
        for i in range(board.width):
            row = []
            for j in range(board.length):
                if(board.board[i][j] is None):
                    row.append(None)
                else:
                    # print(type(board.board[i][j]))
                    row.append((board.board[i][j].nazwa, board.board[i][j].rotacja))
            print(row)

    def print_game_state(self, game):
        print("\n---------------------------\n")
        print("Faza:", game.faza)
        print("Current frakcja:", game.current_frakcja)
        print("User actions:", game.user_actions)
        print("Board:")
        self.print_board(game.board)
        # print("Pile:", game.pile)
        print("Hand:", game.hand)
        # print("Available actions:")
        self.print_available_actions(game.available_actions)
        print("\n---------------------------\n")

    def print_available_actions(self, available_actions):
        print("Available actions:")
        print("Hand:", available_actions["hand"])
        print("Board:")
        for row in available_actions["board"]:
            for hex in row:
                print(hex, end=" ")
            print()
        print("Bottoms:", available_actions["bottoms"])

    #############################################################################
    #   user_available_actions functions       
    #############################################################################
    def default_available_actions(self, game):
        available = deepcopy(self.available_structure)
        if(self.koniec_tury(game, check=True)):
            available["bottoms"]["koniec tury"] = True
        
        game.board.update_available_hexs(False)
        available["hand"] = True

        self.update_available_actions(game, available)

    def update_hand_available_actions(self, current_frakcja, hand, available_hand):
        actions = {key : [False for i in range(self.MAX_HAND_SIZE)] for key in hand.keys()}
        if(not available_hand):
            return actions
        
        for i in range(self.MAX_HAND_SIZE):
            if(self.get_from_hand(hand[current_frakcja], i) is not None):
                actions[current_frakcja][i] = True

        return actions

    def update_available_actions(self, game, available_actions):
        # print("AVAILABLE ACTIONS:", available_actions)
        game.available_actions = {}
        game.available_actions["hand"] = self.update_hand_available_actions(game.current_frakcja, game.hand, available_actions["hand"])
        game.available_actions["board"] = game.board.available_hexs
        game.available_actions["bottoms"] = available_actions["bottoms"]


    #############################################################################
    #   Handler functions      
    #############################################################################
    def handle_hand(self, game, actions, action):
        hand = game.hand[game.current_frakcja]
        zeton = self.get_from_hand(hand, action["slot"])
        action = self.get_first(actions)
        if(action is None):
            self.hand_available_actions(game)
            return None
            
        return self.from_hand(game, action, zeton)

    def handle_rotate(self, game, actions, action):
        x = action["x"]
        y = action["y"]
        rotation = action["rotation"]
        game.board.rotate(x, y, rotation)
        return True

    def handle_done(self, game, actions, action):
        if(not self.koniec_tury(game)):
            return False

        self.poczatek_tury(game)
        return True


    # def handle_cancel(self, game, actions, action):
    #     return True


    def handler(self, game):
        # print("USER ACTIONS:", game.user_actions)
        actions = deepcopy(game.user_actions)
        action = self.get_first(actions)
        if(action is None):
            return
        
        function = self.handlers.get(action["type"], None)
        if(function is not None):
            status = function(game, actions, action)
            if(status is None):
                return None

            # self.default_available_actions(game)
            if(status):
                # game.user_actions.clear()
                return True

            if(not status):
                self.invalid_move(game.user_actions)
                return False
            
        else:
            self.invalid_move(game.user_actions)
            return


    # def bitwa(board):

    #     for inicjatywa in range(9, -1, -1):
    #         for i in range(5):
    #             for j in range(9):
    #                 if board[i][j] is not None:
    #                     board[i][j].aktywuj(inicjatywa)

    #         for i in range(5):
    #             for j in range(9):
    #                 if board[i][j] is not None:
    #                     board[i][j].koniec_inicjatywy()
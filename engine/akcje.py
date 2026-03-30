from copy import deepcopy

def dobierz(hand, pile, nazwa):
    hand.append(nazwa)
    pile.remove(nazwa)

def odrzuc(hand, zeton):
    hand.remove(zeton)

def dociag(hand, pile):
    while(len(hand) < 3 and len(pile) > 0):
            dobierz(hand, pile, pile[-1])

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
def get_from_hand(hand, click):
    if(not isinstance(click, int)):
        return None

    if(len(hand) <= click):
        return None

    return hand[click]

def invalid_move(user_actions):
    print("INVALID MOVE")
    user_actions.clear()
   
def poczatek_tury(game):
    if(game.current_frakcja != None):
        return
    frakcja = game.next_turns[0]["frakcja"]
    typ = game.next_turns[0]["typ"]
    
    # if(frakcja == "bitwa"):
    #     bitwa()
    #     return

    game.current_frakcja = frakcja
    if(typ == "wystaw_sztab"):
        dobierz(game.hand[frakcja], game.pile[frakcja], "sztab")

    else:
        dociag(game.hand[frakcja], game.pile[frakcja])

    if(len(game.pile[frakcja]) == 0):
        game.next_turns.append({"frakcja" : "bitwa", "typ" : "ostatnia"})

def koniec_tury(game):

    frakcja = game.next_turns[0]["frakcja"]
    typ = game.next_turns[0]["typ"]
    
    if((typ == "wystaw_sztab") and (len(game.hand[frakcja]) > 0)):
        invalid_move(game.user_actions)
        return

    if(frakcja == "bitwa"):
        game.user_actions.clear()
        game.next_turns.pop(0)
        if(typ == "ostatnia"):
            game.game_over = 1
            return
    
    if(len(game.hand[frakcja]) == 3):
        invalid_move(game.user_actions)
        return
    
    game.next_turns.pop(0)
    game.next_turns.append({"frakcja" : frakcja, "typ" : "tura"})
    game.current_frakcja = None

def postaw_zeton(board, hand, frakcja, nazwa, x, y):
    odrzuc(hand, nazwa)
    zeton = {"nazwa" : nazwa, "frakcja" : frakcja, "rany" : 0, "rotacja" : 0}
    board.postaw_zeton(x, y, zeton)

def get_first(actions):
    if(actions is None or len(actions) == 0):
        return None
    
    return actions.pop(0)

def wstawianie(board, hand, action, zeton, frakcja):
    x = action["x"]
    y = action["y"]

    if(not board.on_board(x, y)):
        return False

    if(not board.is_empty(x, y)):
        return False
    
    postaw_zeton(board, hand, frakcja, zeton, x, y)
    return True

def from_hand(game, action, zeton):
    hand = game.hand[game.current_frakcja]
    if(zeton is None):
        return False

    if(action["type"] == "board"):
        status = wstawianie(game.board, hand, action, zeton, game.current_frakcja)
        return status

    elif(action["type"] == "odrzuc"):
        odrzuc(hand, zeton)
        # game.user_actions.clear()
        return True
    
    else:
        return False
    
    
def co_zrobic(game):
    print("USER ACTIONS:", game.user_actions)
    actions = deepcopy(game.user_actions)
    action = get_first(actions)

    if(action is None):
        return

    if(action["type"] == "done"):
        koniec_tury(game)
        game.user_actions.clear()
        poczatek_tury(game)
        return
    
    elif(action["type"] == "rotate"):
        x = action["x"]
        y = action["y"]
        rotation = action["rotation"]
        game.board.rotate(x, y, rotation)
        game.user_actions.clear()
        return
        
    elif(action["type"] == "hand"):
        hand = game.hand[game.current_frakcja]
        zeton = get_from_hand(hand, action["slot"])
        action = get_first(actions)
        if(action is None):
            return
        
        status = from_hand(game, action, zeton)
        if(status == False):
            invalid_move(game.user_actions)
            return
        else:
            game.user_actions.clear()
            return
        
    else:
        invalid_move(game.user_actions)
        return
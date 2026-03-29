
def dobierz(hand, pile, frakcja, nazwa):
    hand.append(nazwa)
    pile.remove(nazwa)

def odrzuc(hand, zeton):
    hand.remove(zeton)

def dociag(hand, pile, frakcja):
    while(len(hand) < 3 and len(pile) > 0):
            dobierz(hand, pile, frakcja, pile[-1])

def bitwa(board):

    for inicjatywa in range(9, -1, -1):
        for i in range(5):
            for j in range(9):
                if board[i][j] is not None:
                    board[i][j].aktywuj(inicjatywa)

        for i in range(5):
            for j in range(9):
                if board[i][j] is not None:
                    board[i][j].koniec_inicjatywy()


def invalid_move(user_actions):
    print("INVALID MOVE")
    user_actions.clear()
   
def poczatek_tury(game):
    if(game.current_frakcja != None):
        return
    frakcja = game.next_turns[0]["frakcja"]
    typ = game.next_turns[0]["typ"]
    
    if(frakcja == "bitwa"):
        bitwa()
        return

    game.current_frakcja = frakcja
    if(typ == "wystaw_sztab"):
        dobierz(game.hand[frakcja], game.pile[frakcja], frakcja, "sztab")

    else:
        dociag(game.hand[frakcja], game.pile[frakcja], frakcja)

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
    
    game.user_actions.clear()
    game.next_turns.pop(0)
    game.next_turns.append({"frakcja" : frakcja, "typ" : "tura"})
    game.current_frakcja = None

def postaw_zeton(board, hand, frakcja, nazwa, x, y):
    odrzuc(hand, nazwa)
    zeton = {"nazwa" : nazwa, "frakcja" : frakcja, "rany" : 0, "rotacja" : 0}
    board.postaw_zeton(x, y, zeton)

def obracanie(game):
    actions = game.user_actions
    print("akcje:", actions)

    if(len(actions) <= 1):
        return
    x = actions[0]
    y = actions[1]
    
    idx = 2

    click = actions[idx]
    idx += 1
    print("click:", click)
    if(click == "koniec"):
        game.faza = "gra"
        actions.clear()
        return
    
    if(not isinstance(click, int)):
        invalid_move(actions)
        actions.append(x)
        actions.append(y)
        return

    game.board.obruc(x, y, click)
    actions.pop(-1)
    

def co_zrobic(game):
    if(game.faza == "obruc"):
        obracanie(game)
        return

    actions = game.user_actions
    print("akcje:", actions)
    if(len(actions) == 0):
        return
    click = actions[0]
    idx = 1

    if(click == "koniec"):
        koniec_tury(game)
        poczatek_tury(game)
    
    elif(click == "hand"):
        click = actions[idx]
        idx += 1

        hand = game.hand[game.current_frakcja]

        if(len(hand) <= click):
            invalid_move(actions)
            return


        if(idx >= len(actions)):
            return

        zeton = hand[click]
        click = actions[idx]
        idx += 1
        if(click == "plansza"):
            x = actions[idx]
            idx += 1
            y = actions[idx]
            idx += 1
            if(not game.board.is_empty(x, y)):
                invalid_move(actions)
                return
            
            postaw_zeton(game.board, hand, game.current_frakcja, zeton, x, y)
            actions.clear()
            game.faza = "obruc"
            actions.append(x)
            actions.append(y)
            return

        elif(click == "odrzuc"):
            odrzuc(hand, zeton)
            actions.clear()
            return
        
        else:
            invalid_move(actions)
            return
        
    else:
        invalid_move(actions)
        return
from variable import *
from copy import deepcopy
from variable import *

class InstantToken:

    def __init__(self, name, fraction=None):
        super().__init__(name, fraction)
        # self.name = name
        self.use_handlers = {
            TokenType.Instant.BITWA : self.use_bitwa,
            TokenType.Instant.MOVE : self.use_move,
            TokenType.Instant.BOMB : self.use_bomb,
            TokenType.Instant.GRENADE : self.use_grenade,
            TokenType.Instant.SNIPER : self.use_sniper,
            TokenType.Instant.PUSH : self.use_push,
        }
        self.available_actions_handlers = {
            TokenType.Instant.BITWA : self.available_actions_bitwa,
            TokenType.Instant.MOVE : self.available_actions_move,
            TokenType.Instant.BOMB : self.available_actions_bomb,
            TokenType.Instant.GRENADE : self.available_actions_grenade,
            TokenType.Instant.SNIPER : self.available_actions_sniper,
            TokenType.Instant.PUSH : self.available_actions_push,
        }
        self.use = self.use_handlers.get(name, None)
        self.get_available_actions = self.available_actions_handlers.get(name, None)

    def resolve(self, game, mode):
        if(mode == Mode.AVAILABLE_ACTIONS):
            if(self.available_actions):
                self.available_actions(game)
        if(mode == Mode.USE):
            if(self.use):
                return self.use(game)
        return False

    #############################################################################
    #   Bitwa functions       
    #############################################################################

    def available_actions_bitwa(self, game):
        # print("bitwa available actions")
        available = deepcopy(game.available_structure)
        game.board.update_available_hexs([], [], None)
        if(game.actions.koniec_tury(game, True)):
            available[UI.BOTTOM][Bottom.USE] = True

        available[UI.BOTTOM][Bottom.DISCARD] = True
        # print("available:", available)
        game.actions.update_available_actions(game, available)

    def use_bitwa(self, game):
        game.actions.odrzuc(game.hand[game.current_frakcja], InstantType.BITWA)
        game.actions.koniec_tury(game)
        game.next_turns.insert(0, {Turn.FRACTION : Turn.BITWA, Turn.TYPE : None})
        game.actions.poczatek_tury(game)
        return True

    #############################################################################
    #   Move functions       
    #############################################################################

    def available_actions_move(self, game):
        available = deepcopy(game.available_structure)
        # print("move available actions:", available)

        if(game.state == State.SELECTED_HAND):
            game.board.update_available_hexs([game.current_frakcja], game.board.ALL_HEXES, game.board.can_move)
            available[UI.BOTTOM][Bottom.DISCARD] = True
            available[UI.BOTTOM][Bottom.CANCEL] = True
        
        if(game.state == State.MOVING):
            x = game.selected[Selected.X]
            y = game.selected[Selected.Y]
            adj = game.board.adjacent_hexes(x, y)
            # print(adj)
            game.board.update_available_hexs([None], adj, None)
            game.board.available_hexs[x][y] = True
            # print(game.board.available_hexs)
            available[UI.BOTTOM][Bottom.CANCEL] = True

        game.actions.update_available_actions(game, available)

    def use_move(self, game):
        action = game.action
        # print("state:", game.state)
        if(game.state == State.SELECTED_HAND):
            x = action[Action.Key.X]
            y = action[Action.Key.Y]
            name = game.board.get_name(x, y)
            game.state = State.MOVING
            game.selected = {Selected.X : x, Selected.Y : y, Selected.NAME : name}
            return True

        if(game.state == State.MOVING):
            # print("finishing move...")
            x = game.selected[Selected.X]
            y = game.selected[Selected.Y]
            nx = action[Action.Key.X]
            ny = action[Action.Key.Y]              
            game.board.przenies(x, y, nx, ny)
            game.state = State.ROTATE
            game.selected[Selected.X] = nx
            game.selected[Selected.Y] = ny
            game.active_action = None
            game.actions.odrzuc(game.hand[game.current_frakcja], InstantType.MOVE)
            print(game.state)
            
        return True
    
    #############################################################################
    #   Bomb functions       
    #############################################################################

    def available_actions_bomb(self, game):
        # print("bomb available actions")
        available = deepcopy(game.available_structure)
        available[UI.BOTTOM][Bottom.DISCARD] = True
        available[UI.BOTTOM][Bottom.CANCEL] = True
        game.board.update_available_hexs(Variable.ALL, game.board.ALL_HEXES, game.board.not_on_bound)
        game.actions.update_available_actions(game, available)
    
    def use_bomb(self, game):
        action = game.action
        x = action[Action.Key.X]
        y = action[Action.Key.Y]
        targets = [(x, y)] + game.board.adjacent_hexes(x, y)
        for (x, y) in targets:
            if(game.board.get_name(x, y) == Token.Type.Board.HQ):
                continue
            game.board.deal_damage(x, y, 1)
        
        game.board.zdejmij_trupy()
        game.actions.odrzuc(game.hand[game.current_frakcja], InstantType.BOMB)
        game.actions.prepare_for_new_action(game)
        return True
    
    #############################################################################
    #   Grenade functions       
    #############################################################################

    def available_actions_grenade(self, game):
        available = deepcopy(game.available_structure)
        available[UI.BOTTOM][Bottom.DISCARD] = True
        available[UI.BOTTOM][Bottom.CANCEL] = True

        hq = game.board.find_zeton(Token.Type.Board.HQ, game.current_frakcja)
        print("HQ found at:", (hq.x, hq.y))
        if(not hq.czy_zasieciowany()):
            fractions = [game.enemy[game.current_frakcja]]
            hexes = game.board.adjacent_hexes(hq.x, hq.y)
            game.board.update_available_hexs(fractions, hexes, game.board.not_is_hq)
        game.actions.update_available_actions(game, available)

    def use_grenade(self, game):
        action = game.action
        x = action[Action.Key.X]
        y = action[Action.Key.Y]
        game.board.deal_damage(x, y, 100)
        game.board.zdejmij_trupy()
        game.actions.odrzuc(game.hand[game.current_frakcja], InstantType.GRENADE)
        game.actions.prepare_for_new_action(game)

    #############################################################################
    #   Sniper functions       
    #############################################################################

    def available_actions_sniper(self, game):
        available = deepcopy(game.available_structure)
        available[UI.BOTTOM][Bottom.DISCARD] = True
        available[UI.BOTTOM][Bottom.CANCEL] = True

        game.board.update_available_hexs([game.enemy[game.current_frakcja]], game.board.ALL_HEXES, game.board.not_is_hq)
        game.actions.update_available_actions(game, available)
    
    def use_sniper(self, game):
        action = game.action
        x = action[Action.Key.X]
        y = action[Action.Key.Y]
        game.board.deal_damage(x, y, 1)
        game.board.zdejmij_trupy()
        game.actions.odrzuc(game.hand[game.current_frakcja], InstantType.SNIPER)
        game.actions.prepare_for_new_action(game)

    #############################################################################
    #   Push functions       
    #############################################################################

    def available_actions_push(self, game):
        available = deepcopy(game.available_structure)
        if(game.state == State.SELECTED_HAND):
            game.board.update_available_hexs([game.current_frakcja], game.board.ALL_HEXES, game.board.can_push)
            available[UI.BOTTOM][Bottom.DISCARD] = True
            available[UI.BOTTOM][Bottom.CANCEL] = True

        elif(game.state == State.SELECTED_PUSHER):
            print("selected pusher available actions")
            x = game.selected[Selected.X]
            y = game.selected[Selected.Y]
            adj = game.board.adjacent_hexes(x, y)
            print("adjacent hexes:", adj)
            game.board.update_available_hexs([game.enemy[game.current_frakcja]], adj, game.board.can_move)
            available[UI.BOTTOM][Bottom.CANCEL] = True
        
        elif(game.state == State.PUSHING):
            x = game.selected[Selected.X]
            y = game.selected[Selected.Y]
            px = game.selected[Selected.PUSHER_X]
            py = game.selected[Selected.PUSHER_Y]

            my_adj = game.board.adjacent_hexes(x, y)
            pusher_adj = game.board.adjacent_hexes(px, py)
            adj = []
            for hex in my_adj:
                if(hex not in pusher_adj):
                    adj.append(hex)
            game.board.update_available_hexs([None], adj, None)
        
        game.actions.update_available_actions(game, available)

    def use_push(self, game):
        # print("using push...")
        action = game.action
        if(game.state == State.SELECTED_HAND):
            x = action[Action.Key.X]
            y = action[Action.Key.Y]
            name = game.board.get_name(x, y)
            game.state = State.SELECTED_PUSHER
            game.selected = {Selected.X : x, Selected.Y : y, Selected.NAME : name}
            game.active_action = InstantType.PUSH
            return True

        elif(game.state == State.SELECTED_PUSHER):
            # print("selected pusher:", game.selected)
            x = action[Action.Key.X]
            y = action[Action.Key.Y]
            name = game.board.get_name(x, y)
            px = game.selected[Selected.X]
            py = game.selected[Selected.Y]
            game.selected = {Selected.X : x, Selected.Y : y, Selected.NAME : name}
            game.selected[Selected.PUSHER_X] = px
            game.selected[Selected.PUSHER_Y] = py
            game.state = State.PUSHING
            game.active_action = InstantType.PUSH
            # print("enemy fraction:", game.enemy[game.current_frakcja])
            game.current_frakcja = game.enemy[game.current_frakcja]
            # print("state after selecting target:", game.current_frakcja, game.state)
            return True

        elif(game.state == State.PUSHING):
            target_x = game.selected[Selected.X]
            target_y = game.selected[Selected.Y]
            nx = action[Action.Key.X]
            ny = action[Action.Key.Y]
            game.board.przenies(target_x, target_y, nx, ny)
            game.current_frakcja = game.enemy[game.current_frakcja]
            game.actions.odrzuc(game.hand[game.current_frakcja], InstantType.PUSH)
            game.actions.prepare_for_new_action(game)
            return True

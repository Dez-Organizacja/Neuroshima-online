from main.board.board import Board
from main.tokens.board_token import BoardToken
# from main.tokens.ability import Ability
from main.tokens.data import TokenRelation
from main.utils.variable import Boost, Attack

class BoosterSolver():
    board: Board
    boosts: list[tuple[int, Boost]] # (tokenID -> to, boost)]
    steal_boosts: list[tuple[int, Boost]] # (tokenID -> from, boost)]
    
    def __init__(self, board: Board) -> None:
        self.board = board
        self.boosts = []
        self.steal_boosts = []

        self.kastrando_las_boosten()

        self.collect_steal_boosts()
        self.solve_steal_boosts()

        self.collect_boosts(self.boosts)
        self.solve_all()
        self.end_booster_faze()

    def kastrando_las_boosten(self):
        for board_hex in self.board.ALL_HEXES:
            tokenID = self.board.gen_tokenID(board_hex)
            if tokenID is None:
                continue

            token = self.board.tokens[tokenID]
            token.BOOST_TARGET = token.REAL_BOOST_TARGET
            token.MEELE_BOOSTS = 0
            token.SHOOT_BOOSTS = 0
            token.CLEVER_INICIATIVE.begin_iniciative()

    def is_valid_target(self, tokenID : int, relation : TokenRelation, my_fraction : str) -> bool:
        if (tokenID is None):
            return False
        if (relation == TokenRelation.OWN):
            return self.board.tokens[tokenID].faction == my_fraction
        elif (relation == TokenRelation.ENEMY):
            return self.board.tokens[tokenID].faction != my_fraction
        elif (relation == TokenRelation.ALL):
            return True
        return False

    def collect_steal_boosts(self):
        for board_hex in self.board.ALL_HEXES:
            tokenID = self.board.gen_tokenID(board_hex)
            if tokenID is None:
                continue

            token = self.board.tokens[tokenID]
            if len(token.BOOSTS) > 0 and Boost.STEAL_BOOST in token.BOOSTS and not token.is_wired():
                for direction in token.BOOSTS[Boost.STEAL_BOOST]:
                    target_pos = self.board.go(board_hex, direction)
                    if not self.board.on_board(target_pos):
                        continue
                    target_tokenID = self.board.gen_tokenID(target_pos)
                    if self.is_valid_target(target_tokenID, token.BOOST_TARGET, token.faction):
                        self.steal_boosts.append((target_tokenID, Boost.STEAL_BOOST))

    def solve_steal_boosts(self):
        for tokenID, boost in self.steal_boosts:
            token = self.board.tokens[tokenID]
            if token is not None:
                token.BOOST_TARGET = TokenRelation.ENEMY

    def collect_boosts(self, list_of_boosts : list):
        for board_hex in self.board.ALL_HEXES:
            tokenID = self.board.gen_tokenID(board_hex)
            if tokenID is None:
                continue

            token = self.board.tokens[tokenID]
            if not token.is_wired():
                for boost_type, boosts in token.BOOSTS.items():
                    if boost_type == Boost.STEAL_BOOST:
                        continue
                    for direction in boosts:
                        target_pos = self.board.go(board_hex, direction)
                        if not self.board.on_board(target_pos):
                            continue
                        target_tokenID = self.board.gen_tokenID(target_pos)
                        if self.is_valid_target(target_tokenID, token.BOOST_TARGET, token.faction):
                            list_of_boosts.append((target_tokenID, boost_type))

    def solve_all(self):
        for tokenID, boost_type in self.boosts:
            handler = getattr(self, boost_type.name, None)
            if handler is not None:
                handler(tokenID)

    def end_booster_faze(self):
        for token in self.board.tokens.values():
            token.CLEVER_INICIATIVE.end_booster_faze()

    def MELEE(self, tokenID):
        self.board.tokens[tokenID].MEELE_BOOSTS += 1

    def MEELE(self, tokenID):
        self.MELEE(tokenID)

    def SHOOT(self, tokenID):
        self.board.tokens[tokenID].SHOOT_BOOSTS += 1

    def INITIATIVE(self, tokenID):
        self.board.tokens[tokenID].CLEVER_INICIATIVE.iniciative_boosts += 1

    def INICIATIVE(self, tokenID):
        self.INITIATIVE(tokenID)
    
    def MINUS_INITIATIVE(self, tokenID):
        self.board.tokens[tokenID].CLEVER_INICIATIVE.iniciative_boosts -= 1
 
    def NEW_INITIATIVE(self, tokenID):
        self.board.tokens[tokenID].CLEVER_INICIATIVE.num_of_new += 1

    def NEW_INICIATIVE(self, tokenID):
        self.NEW_INITIATIVE(tokenID)

    def SET_INITIATIVE_TO_0(self, tokenID):
        self.board.tokens[tokenID].CLEVER_INICIATIVE.is_blocked_to_0 = True
    
    def MEELE_TO_SHOOT(self, tokenID):
        return NotImplemented

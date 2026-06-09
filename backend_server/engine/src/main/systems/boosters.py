from main.board.board import Board
from main.tokens.data import TokenRelation, Boost
from main.systems.clever_initiative import CleverInitiative

class BoosterSolver():
    board: Board
    boosts: list[tuple[int, Boost]] # (tokenID -> to, boost)]
    steal_boosts: list[tuple[int, Boost]] # (tokenID -> from, boost)]
    
    @classmethod
    def compute(cls, board : Board):
        cls(board)

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
            relations = token.state.relations
            relations.real_boost_target = token.config.boost_target

            token.state.modifiers.meele_boosts = 0
            CleverInitiative.begin_initiative(token)

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
            if Boost.STEAL_BOOST in token.boosts and not token.wired:
                for direction in token.get_boost_directions(Boost.STEAL_BOOST):
                    target_pos = self.board.go(board_hex, direction)
                    if not self.board.on_board(target_pos):
                        continue
                    target_tokenID = self.board.gen_tokenID(target_pos)
                    if self.is_valid_target(target_tokenID, token.state.relations.real_boost_target, token.faction):
                        self.steal_boosts.append((target_tokenID, Boost.STEAL_BOOST))

    def solve_steal_boosts(self):
        for tokenID, boost in self.steal_boosts:
            token = self.board.tokens[tokenID]
            if token is not None:
                token.state.relations.real_boost_target = TokenRelation.ENEMY

    def collect_boosts(self, list_of_boosts : list):
        for board_hex in self.board.ALL_HEXES:
            tokenID = self.board.gen_tokenID(board_hex)
            if tokenID is None:
                continue

            token = self.board.tokens[tokenID]
            if not token.wired:
                for boost_type in token.boosts.keys():
                    if boost_type == Boost.STEAL_BOOST:
                        continue
                    for direction in token.get_boost_directions(boost_type):
                        target_pos = self.board.go(board_hex, direction)
                        if not self.board.on_board(target_pos):
                            continue
                        target_tokenID = self.board.gen_tokenID(target_pos)
                        if self.is_valid_target(target_tokenID, token.state.relations.real_boost_target, token.faction):
                            list_of_boosts.append((target_tokenID, boost_type))

    def solve_all(self):
        for tokenID, boost_type in self.boosts:
            handler = getattr(self, boost_type.name.lower(), None)
            if handler is not None:
                handler(tokenID)

    def end_booster_faze(self):
        for token in self.board.tokens.values():
            CleverInitiative.end_booster_faze(token)

    def melee(self, tokenID):
        self.board.tokens[tokenID].state.modifiers.meele_boosts += 1

    def initiative(self, tokenID):
        self.board.tokens[tokenID].clever_initiative.initiative_boosts += 1

    def minus_initiative(self, tokenID):
        self.board.tokens[tokenID].clever_initiative.initiative_boosts -= 1
 
    def new_initiative(self, tokenID):
        self.board.tokens[tokenID].clever_initiative.num_of_new += 1

    def set_initiative_to_0(self, tokenID):
        self.board.tokens[tokenID].clever_initiative.is_blocked_to_0 = True
    
    def meele_to_shoot(self, tokenID):
        return NotImplemented

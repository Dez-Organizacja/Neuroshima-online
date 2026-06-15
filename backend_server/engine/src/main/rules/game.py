from main.utils.variable import Phase
from main.tokens.board_token import BoardToken
from main.board.board import Board

class GameRules():
    @staticmethod
    def get_enemy(factions : list[str], my_faction):
        # print(f"getting enemy of {my_faction}")
        for faction in factions:
            if(faction != my_faction):
                # print(f"found enemy {faction}")
                return faction

    @staticmethod
    def get_score(board : Board, faction : str) -> int:
        pos = board.get_hq_pos(faction)
        if pos is None:
            return 0
        hq = board.get_token(pos)
        return max(0, hq.config.hp - hq.state.damage)

    def get_scores(self, board : Board, factions : list[str]):
        return [
            self.get_score(board, faction)
            for faction in factions
        ]


    def get_winner(self, board : Board, factions : str) -> str | None:
        scores = self.get_scores(board, factions)

        if len(set(scores)) == 1:
            return None
        
        if scores[0] > scores[1]:
            return factions[0]
        
        return factions[1]

    def is_game_over(self, board : Board, factions : str, phase : Phase) -> bool:
        print("game over checking")
        print(f"factions {factions}")
        scores = self.get_scores(board, factions)
        print(f"scores: {scores}")

        if any(score <= 0 for score in scores):
            return True

        if phase == Phase.ENDGAME:
            return len(set(scores)) > 1
        
        return False

from main.utils.variable import Phase
from main.board.board import Board

class GameRules():
    

    # def get_faction(faction : str, relation : TokenRelation)

    @staticmethod
    def get_score(board : Board, faction : str) -> int:
        pos = board.get_hq_pos(faction)
        if pos is None:
            return 0
        hq = board.get_token(pos)
        return max(0, hq.config.hp - hq.state.damage)

    @classmethod
    def get_scores(cls, board : Board, factions : list[str]):
        return [
            cls.get_score(board, faction)
            for faction in factions
        ]

    @classmethod
    def get_winner(cls, board : Board, factions : str) -> str | None:
        scores = cls.get_scores(board, factions)

        if len(set(scores)) == 1:
            return None
        
        if scores[0] > scores[1]:
            return factions[0]
        
        return factions[1]

    @classmethod
    def is_game_over(cls, board : Board, factions : str, phase : Phase) -> bool:
        # print("game over checking")
        print(f"factions {factions}")
        scores = cls.get_scores(board, factions)
        print(f"scores: {scores}")

        if any(score <= 0 for score in scores):
            return True

        if phase == Phase.ENDGAME:
            return len(set(scores)) > 1
        
        return False

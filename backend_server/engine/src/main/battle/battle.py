from main.actions.akcje_na_planszy import AkcjeNaPlanszy

class Battle:
    def __init__(self, ctx):
        # self.game = game
        # self.actions = game.actions
        # self.board = game.board
        self.anp = AkcjeNaPlanszy(ctx.board)

        self.run(ctx)

        # self.actions.koniec_tury(game)
        # self.actions.poczatek_tury(game)

    def run_initiative(self, inicjatywa):
        self.anp.reset_all()
        self.anp.kwestia_sieciarzy()
        self.anp.boost_all()
        self.anp.aktywacja(inicjatywa)
        self.anp.zdejmij_trupy()

    def run(self, ctx):
        for inicjatywa in range(ctx.board.max_inicjatywa, -1, -1):
            self.run_initiative(inicjatywa)

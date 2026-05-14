
# class BattleRules:
    # def get_av

    # def available_actions_bitwa(self, ctx):
    #     wanted_bootoms = [Bottom.USE, Bottom.DISCARD, Bottom.CANCEL]
    #     return AvailableActionResult(
    #         bottoms=self.get_availabe_bottoms(ctx, wanted_bootoms)
    #     )
          
    #############################################################################
    #   Bomb functions       
    #############################################################################

    # def available_actions_bomb(self, ctx):
    #     query = BoardQuery([ctx.rules.is_not_on_border])
    #     return AvailableActionResult(
    #         positions=query.apply(ctx),
    #         bottoms=self.default_bottoms(ctx)      
    #     )
    #############################################################################
    #   Grenade functions       
    #############################################################################

    # def available_actions_grenade(self, ctx):
    #     positions = []
    #     # pos = ctx.board.find_zeton(BoardType.HQ, ctx.fraction)
    #     # tile = ctx.board.get_tile(pos)
    #     pos = ctx.board.get_hq_pos(ctx.fraction)
    #     if ctx.rules.is_hq_not_wired(ctx.fraction):
    #         query = BoardQuery([
    #             ctx.rules.adjacent_to(pos),
    #             ctx.rules.is_enemy_at,
    #             ctx.rules.not_hq_at
    #         ])

    #     return AvailableActionResult(
    #         positions = query.apply(ctx),
    #         bottoms = self.default_bottoms(ctx)
    #     )
    #############################################################################
    #   Sniper functions       
    #############################################################################

    # def available_actions_sniper(self, ctx):
    #     # rules = ctx.rules
    #     query = BoardQuery([
    #         ctx.rules.is_enemy_at,
    #         ctx.rules.not_hq_at
    #     ])
    #     return AvailableActionResult(
    #         positions=query.apply(ctx),  
    #         bottoms = self.default_bottoms(ctx)
    #     )
from main.utils.variable import *
from main.tokens.abstract_token import Token
from main.board.board_query import BoardQuery
from main.actions.available.result import AvailableActionResult
from main.actions.execute.result import ActionResult
from main.effects.board_effects import *
from main.effects.flow_effects import StartBattleEvent, SwapPlayerEvent
from main.effects.ui_change_effects import SetInteractionState, SetSelected, ResetInteraction
from main.state.selection import Selected

class InstantToken(Token):
    # TYPE = "instant"

    def __init__(self, rules, name, fraction):
        super().__init__(rules, name, fraction, TokenType.INSTANT)
        self.execute_handlers = {
            InstantType.BITWA : self.execute_bitwa,
            InstantType.MOVE : self.execute_move,
            InstantType.BOMB : self.execute_bomb,
            InstantType.GRENADE : self.execute_grenade,
            InstantType.SNIPER : self.execute_sniper,
            InstantType.PUSH : self.execute_push,
        }
        self.available_actions_handlers = {
            InstantType.BITWA : self.available_actions_bitwa,
            InstantType.MOVE : self.available_actions_move,
            InstantType.BOMB : self.available_actions_bomb,
            InstantType.GRENADE : self.available_actions_grenade,
            InstantType.SNIPER : self.available_actions_sniper,
            InstantType.PUSH : self.available_actions_push,
        }


    def export(self):
        return self.name

    def get_available_actions(self, ctx):
        handler = self.available_actions_handlers.get(self.name, None)
        if handler:
            return handler(ctx)
        return AvailableActionResult()
    
    def execute(self, ctx, action):
        handler = self.execute_handlers.get(self.name, None)
        if handler:
            return handler(ctx, action)
    
    def default_bottoms(self, ctx):
        wanted_bottoms = [Bottom.DISCARD, Bottom.CANCEL]
        return self.get_availabe_bottoms(ctx, wanted_bottoms)
    
    def get_availabe_bottoms(self, ctx, wanted):
        return ctx.rules.get_available_bottoms(ctx, wanted)
    #############################################################################
    #   Bitwa functions       
    #############################################################################

    # def available_actions_bitwa(self, ctx):
    #     wanted_bootoms = [Bottom.USE, Bottom.DISCARD, Bottom.CANCEL]
    #     return AvailableActionResult(
    #         bottoms=self.get_availabe_bottoms(ctx, wanted_bootoms)
    #     )

    def execute_bitwa(self, ctx, action):
        return ActionResult(
            effects=[DiscardActiveTokenEffect()],
            flow_events=[StartBattleEvent()]
        )
        # actions = ctx.actions
        # state = ctx.state

        # ctx.player.hand.discard_active_token()
        # actions.koniec_tury(state)
        # state.next_turns.insert(0, {Turn.FRACTION : Turn.BITWA, Turn.TYPE : None})
        # actions.poczatek_tury(state)

    #############################################################################
    #   Move functions       
    #############################################################################

    
    def execute_move(self, ctx, action):
        # state = ctx.state
        # action = state.action
        if(ctx.ui_state == State.SELECTED_HAND):
            pos = action[Action.Key.POS]
            return ActionResult(
                interaction_state_changes=[
                    SetInteractionState(State.MOVING),
                    SetSelected(Selected(pos))
                ]
            )
            # state.interaction_state = State.MOVING
            # state.selected.unit_position = pos
            # state.selected = {
            #     Selected.POS : pos, 
            #     Selected.NAME : ctx.board.get_name(pos)
            # }

        if(ctx.ui_state == State.MOVING):
            old_pos = ctx.selected.unit_position
            new_pos = action[Action.Key.POS]
            return ActionResult(
                effects=[
                    MoveEffect(old_pos, new_pos),
                    DiscardActiveTokenEffect()
                ],
                interaction_state_changes=[
                    SetInteractionState(State.ROTATE),
                    SetSelected(Selected(new_pos))
                ]
            )
            # ctx.board.przenies(old_pos, new_pos)
            # state.interaction_state = State.ROTATE
            # state.selected.unit_position = new_pos
            # player = state.current_player
            # player.hand.discard_active_token()
          
    #############################################################################
    #   Bomb functions       
    #############################################################################

    # def available_actions_bomb(self, ctx):
    #     query = BoardQuery([ctx.rules.is_not_on_border])
    #     return AvailableActionResult(
    #         positions=query.apply(ctx),
    #         bottoms=self.default_bottoms(ctx)      
    #     )
    
    def execute_bomb(self, ctx, action):
        pos = action[Action.Key.POS]
        targets = [
            pos, 
            *ctx.board.adjacent_hexes(pos)
            ]
        profile = DamageProfile(
            can_hit_hq=False, 
            ignore_armor=True
        )

        return ActionResult(
            effects=[
                DamageEffect(pos = target, power = 1, profile = profile)
                for target in targets
            ] + [DiscardActiveTokenEffect()],
            interaction_state_changes=[
                ResetInteraction()
            ]
        )
        # for target in targets:
        #     if(ctx.board.is_not_hq(target)):
        #         ctx.board.deal_damage(pos, 1)
        
        # ctx.board.zdejmij_trupy()
        # ctx.player.hand.discard_active_token()
        # ctx.actions.prepare_for_new_action(ctx.state)
    
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

    def execute_grenade(self, ctx, action):
        pos = action[Action.Key.POS]
        profile = DamageProfile(can_hit_hq=False, ignore_armor=True)
        return ActionResult(
            effects=[
                DamageEffect(
                    pos = pos,
                    power=100,
                    profile=profile
                ),
                DiscardActiveTokenEffect()
            ],
            interaction_state_changes=[
                ResetInteraction()
            ]
        )
        # ctx.board.deal_damage(pos, 100)
        # ctx.board.zdejmij_trupy()
        # ctx.player.hand.discard_active_token()
        # ctx.actions.prepare_for_new_action(ctx.state)

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

    
    def execute_sniper(self, ctx, action):
        pos = action[Action.Key.POS]
        profile = DamageProfile(can_hit_hq=False, ignore_armor=True)
        return ActionResult(
            effects=[
                DamageEffect(
                    pos = pos,
                    power = 1,
                    profile=profile
                ),
                DiscardActiveTokenEffect()
            ],
            interaction_state_changes=[
                ResetInteraction()
            ]
        )
        # ctx.board.deal_damage(pos, 1)
        # ctx.board.zdejmij_trupy()
        # ctx.player.hand.discard_active_token()

        # ctx.actions.prepare_for_new_action(ctx.state)

    #############################################################################
    #   Push functions       
    #############################################################################
  

    # def available_actions_push(self, ctx):
    #     # state = ctx.state.interaction_state

    #     handler = {
    #         State.SELECTED_HAND: self._push_selected_hand,
    #         State.SELECTED_PUSHER: self._push_selected_pusher,
    #         State.PUSHING: self._push_selected_pushing,
    #     }.get(ctx.ui_state)

    #     if handler:
    #         return handler(ctx)

    #     return AvailableActionResult()

    def execute_push(self, ctx, action):
        if(ctx.ui_state == State.SELECTED_HAND):
            pos = action[Action.Key.POS]
            return ActionResult(
                interaction_state_changes=[
                    SetInteractionState(State.SELECTED_PUSHER),
                    SetSelected(pos)
                ]
            )
            # ctx.state.interaction_state = State.SELECTED_PUSHER
            # ctx.state.selected.unit_position = pos
            # ctx.active_action = InstantType.PUSH
        
        elif(ctx.state.interaction_state == State.SELECTED_PUSHER):
            pos = action[Action.Key.POS]
            pusher_pos = ctx.selected.unit_position
            return ActionResult(
                interaction_state_changes=[
                    SetInteractionState(State.PUSHING),
                    SetSelected(SetSelected(pusher_pos, pos))
                ],
                flow_events=[
                    SwapPlayerEvent(),
                ]
            )
            # ctx.selected.target_position = pos
            # ctx.state.interaction_state = State.PUSHING
            # ctx.state.active_action = InstantType.PUSH
            # ctx.state.current_fraction = ctx.state.get_enemy(ctx.fraction, ctx.state.fractions)
            

        elif(ctx.state.interaction_state == State.PUSHING):
            target_pos = ctx.selected.target_position
            new_pos = action[Action.Key.POS]
            return ActionResult(
                effects=[
                    MoveEffect(target_pos, new_pos),
                    DiscardActiveTokenEffect()
                ],
                interaction_state_changes=[
                    ResetInteraction()
                ],
                flow_events=[
                    SwapPlayerEvent()
                ]
            )
            # ctx.board.przenies(target_pos, new_pos)
            # ctx.state.current_fraction = ctx.state.get_enemy(ctx.fraction, ctx.state.fractions)
            # ctx.player.hand.discard_active_token()
            # ctx.actions.prepare_for_new_action(ctx.state)
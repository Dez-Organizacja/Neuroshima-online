
from main.tokens.data import TokenKey, TokenType, TokenStats, Ability

wlasciwosci = {
    "sieciarz": {
        TokenKey.TYPE: TokenType.BOARD,
        TokenKey.UNIT_COUNT: 10,
        TokenStats.HP: 1,
        TokenStats.WIRE: [0],
        },
    "dwu-sieciarz": {
        TokenKey.TYPE: TokenType.BOARD,
        TokenKey.UNIT_COUNT: 10,
        TokenStats.HP: 1,
        TokenStats.WIRE: [0, 1],
    },
    "snajper": {
        TokenKey.ABILITY : Ability.SNIPER,
        TokenKey.TYPE : TokenType.INSTANT,
        TokenKey.UNIT_COUNT : 1,
    }
}

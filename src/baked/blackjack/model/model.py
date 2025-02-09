import enum


class Play(str, enum.Enum):
    BUST = "BUST"
    DOUBLE = "DOUBLE"
    HIT = "HIT"
    SPLIT = "SPLIT"
    STAND = "STAND"
    SURRENDER = "SURRENDER"


class Card(int, enum.Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ACE = 11


class CardDeck(list):
    
    def __init__(self):
        super().__init__(
            [Card.TWO] * 4 + [Card.THREE] * 4 + [Card.FOUR] * 4 + [Card.FIVE] * 4 + \
            [Card.SIX] * 4 + [Card.SEVEN] * 4 + [Card.EIGHT] * 4 + [Card.NINE] * 4 + \
            [Card.TEN] * 16 + [Card.ACE] * 4
        )

import enum

from typing import List

from baked.blackjack.basicstrategy.charts.h17 import HARD as H17_HARD, PAIR as H17_PAIR, SOFT as H17_SOFT
from baked.blackjack.model.model import Card, Play


class RuleSet(str, enum.Enum):
    H17 = "H17"


class Chart(str, enum.Enum):
    HARD = "HARD"
    SOFT = "SOFT"
    PAIR = "PAIR"


class Rule(str, enum.Enum):
    ALLOW_DOUBLE = "ALLOW_DOUBLE"
    ALLOW_DOUBLE_AFTER_SPLIT = "ALLOW_DOUBLE_AFTER_SPLIT"
    ALLOW_SURRENDER = "ALLOW_SURRENDER"


class Service:

    DATA_ROOT = "~/Work/git/blackjack/data"

    def __init__(self):
        self._ruleset: RuleSet = RuleSet.H17
        self._rules: List[Rule] = []

    def add_rule(self, rule: Rule):
        self._rules.append(rule)

    def get_chart(self, chart: Chart) -> List[List]:
        return {
            RuleSet.H17: {
                Chart.HARD: H17_HARD,
                Chart.PAIR: H17_PAIR,
                Chart.SOFT: H17_SOFT
            }
        }[self._ruleset][chart]

    def get_play(self, cards: List[Card], dealer_card: Card, force_no_pair: bool = False) -> Play:
        
        # Compute hand total
        hand_total = 0
        for c in cards:
            card_value = int(c)
            hand_total += card_value
            if hand_total > 21 and c == Card.ACE:
                hand_total = hand_total - card_value + 1

        is_soft = len(cards) == 2 and (cards[0] == Card.ACE or cards[1] == Card.ACE)
        no_split = len(cards) > 2 or cards[0] != cards[1] or force_no_pair

        # The basics
        if hand_total > 21:
            return Play.BUST
        elif hand_total == 21:
            return Play.STAND
        elif hand_total > 17 and not is_soft and no_split:
            return Play.STAND
        elif hand_total < 8 and no_split:
            return Play.HIT

        # Now we need the charts
        chart_name = None
        lookup = [None, None]
        if len(cards) > 2:
            chart_name = Chart.HARD
            lookup[0] = str(hand_total)
        elif cards[0] == cards[1] and not force_no_pair:
            chart_name = Chart.PAIR
            lookup[0] = "A" if cards[0] == Card.ACE else str(cards[0].value)
        elif is_soft:
            chart_name = Chart.SOFT
            lookup[0] = f"A{cards[0] if cards[0] != Card.ACE else cards[1]}"
        else:
            chart_name = Chart.HARD
            lookup[0] = str(hand_total)

        lookup[1] = "A" if dealer_card == Card.ACE else str(dealer_card.value)
        chart = self.get_chart(chart_name)

        for x in range(1, len(chart)):
            if chart[x][0] == lookup[0]:
                for y, dh in enumerate(chart[0]):
                    if dh == lookup[1]:
                        p = chart[x][y]
                        break

        play = {
            Chart.HARD: {
                "D": Play.DOUBLE if self.double_allowed else Play.HIT,
                "H": Play.HIT,
                "S": Play.STAND,
                "SUR": Play.SURRENDER if self.surrender_allowed else Play.HIT
            },
            Chart.SOFT: {
                "D": Play.DOUBLE if self.double_allowed else Play.HIT,
                "DS": Play.DOUBLE if self.double_allowed else Play.STAND,
                "H": Play.HIT,
                "S": Play.STAND
            },
            Chart.PAIR: {
                "N": None,
                "Y": Play.SPLIT,
                "YN": Play.SPLIT if self.double_after_split_allowed else None
            }
        }[chart_name][p]

        # Recurse with force ignore split here
        if play is None:
            return self.get_play(cards, dealer_card, force_no_pair=True)
    
        return play
    
    @property
    def double_allowed(self) -> bool:
        return Rule.ALLOW_DOUBLE in self._rules
    
    @property
    def double_after_split_allowed(self) -> bool:
        return Rule.ALLOW_DOUBLE_AFTER_SPLIT in self._rules
    
    @property
    def surrender_allowed(self) -> bool:
        return Rule.ALLOW_SURRENDER in self._rules

import random

from baked.blackjack.model.model import Card


class FullPractice:
    """
    Usage:
        Iterator to return all possible permutations for player vs dealer
        for basic strategy practice.
        Each iteration will yield a list where the first element is another list
        (the players hard) and the second element is a Card (the dealers up card).

        [[10,A],A] - Blackjack versus A
        [[8,8], 4] - Pair of 8's versus 4
    """

    def __init__(self, randomize: bool = False):
        self.selections = [[l, r, d] for l in Card for r in Card for d in Card]
        if randomize:
            random.shuffle(self.selections)

    def __iter__(self):
        seen = []
        for left, right, dealer in self.selections:
            if left + right == 21:
                continue
            elif [left, right, dealer] in seen or [right, left, dealer] in seen:
                continue

            seen.append([left, right, dealer])
            yield [[left, right], dealer]

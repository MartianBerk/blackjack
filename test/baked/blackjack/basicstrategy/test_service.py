import unittest

from baked.blackjack.basicstrategy.service import Rule, Service as BasicStrategyService
from baked.blackjack.model.model import Card, Play

class BasicStrategyServiceTests(unittest.TestCase):

    def setUp(self):
        self.service = BasicStrategyService()

    def test_get_play_hard_with_double(self):
        """
        This only tests the deviations when DOUBLE is allowed.
        test_get_play_hard_without_double contains all the possible outcomes.
        """
        test_func = self.service.get_play

        self.service.add_rule(Rule.ALLOW_DOUBLE)

        hands = [
            [Card.THREE, Card.SIX],
            [Card.FOUR, Card.SIX],
            [Card.FIVE, Card.SIX],
        ]

        dealer = [
            Card.TWO, Card.THREE, Card.FOUR, Card.FIVE, Card.SIX,
            Card.SEVEN, Card.EIGHT, Card.NINE, Card.TEN, Card.ACE
        ]

        results = [
            [Play.HIT] + [Play.DOUBLE] * 4 + [Play.HIT] * 5,
            [Play.DOUBLE] * 8 + [Play.HIT] * 2,
            [Play.DOUBLE] * 10,
        ]
        
        for i, h in enumerate(hands):
            for j, d in enumerate(dealer):
                self.assertEqual(test_func(h, d), results[i][j], f"Hand: {h}, Dealer: {d}")

    def test_get_play_hard_without_double(self):
        test_func = self.service.get_play

        hands = [
            [Card.TWO, Card.SIX],
            [Card.THREE, Card.SIX],
            [Card.FOUR, Card.SIX],
            [Card.FIVE, Card.SIX],
            [Card.SEVEN, Card.FIVE],
            [Card.SEVEN, Card.SIX],
            [Card.EIGHT, Card.SIX],
            [Card.NINE, Card.SIX],
            [Card.TEN, Card.SIX],
            [Card.TEN, Card.SEVEN],
            [Card.TEN, Card.EIGHT],
            [Card.TEN, Card.NINE],
            [Card.TEN, Card.TEN],
            [Card.TEN, Card.ACE],
        ]

        dealer = [
            Card.TWO, Card.THREE, Card.FOUR, Card.FIVE, Card.SIX,
            Card.SEVEN, Card.EIGHT, Card.NINE, Card.TEN, Card.ACE
        ]

        results = [
            [Play.HIT] * 10,
            [Play.HIT] * 10,
            [Play.HIT] * 10,
            [Play.HIT] * 10,
            [Play.HIT] * 2 + [Play.STAND] * 3 + [Play.HIT] * 5,
            [Play.STAND] * 5 + [Play.HIT] * 5,
            [Play.STAND] * 5 + [Play.HIT] * 5,
            [Play.STAND] * 5 + [Play.HIT] * 5,
            [Play.STAND] * 5 + [Play.HIT] * 5,
            [Play.STAND] * 10,
            [Play.STAND] * 10,
            [Play.STAND] * 10,
            [Play.STAND] * 10,
            [Play.STAND] * 10,
        ]
        
        for i, h in enumerate(hands):
            for j, d in enumerate(dealer):
                self.assertEqual(test_func(h, d), results[i][j], f"Hand: {h}, Dealer: {d}")

    def test_get_play_hard_with_surrender(self):
        """
        This only tests the deviations when SURRENDER is allowed.
        test_get_play_hard_without_double contains all the possible outcomes.
        """
        test_func = self.service.get_play

        self.service.add_rule(Rule.ALLOW_SURRENDER)

        hands = [
            [Card.NINE, Card.SIX],
            [Card.TEN, Card.SIX],
        ]

        dealer = [
            Card.NINE, Card.TEN, Card.ACE
        ]

        results = [
            [Play.HIT, Play.SURRENDER, Play.HIT],
            [Play.SURRENDER] * 3,
        ]
        
        for i, h in enumerate(hands):
            for j, d in enumerate(dealer):
                self.assertEqual(test_func(h, d), results[i][j], f"Hand: {h}, Dealer: {d}")

    def test_get_play_soft_with_double(self):
        """
        This only tests the deviations when DOUBLE is allowed.
        test_get_play_soft_without_double contains all the possible outcomes.
        """
        test_func = self.service.get_play

        self.service.add_rule(Rule.ALLOW_DOUBLE)

        hands = [
            [Card.TWO, Card.ACE],
            [Card.THREE, Card.ACE],
            [Card.FOUR, Card.ACE],
            [Card.FIVE, Card.ACE],
            [Card.SIX, Card.ACE],
            [Card.ACE, Card.SEVEN],
            [Card.ACE, Card.EIGHT],
        ]

        dealer = [
            Card.TWO, Card.THREE, Card.FOUR, Card.FIVE, Card.SIX,
        ]

        results = [
            [Play.HIT] * 3 + [Play.DOUBLE] * 2,
            [Play.HIT] * 3 + [Play.DOUBLE] * 2,
            [Play.HIT] * 2 + [Play.DOUBLE] * 3,
            [Play.HIT] * 2 + [Play.DOUBLE] * 3,
            [Play.HIT] * 1 + [Play.DOUBLE] * 4,
            [Play.DOUBLE] * 5,
            [Play.STAND] * 4 + [Play.DOUBLE] * 1,
        ]
        
        for i, h in enumerate(hands):
            for j, d in enumerate(dealer):
                self.assertEqual(test_func(h, d), results[i][j], f"Hand: {h}, Dealer: {d}")

    def test_get_play_soft_without_double(self):
        test_func = self.service.get_play

        hands = [
            [Card.TWO, Card.ACE],
            [Card.THREE, Card.ACE],
            [Card.FOUR, Card.ACE],
            [Card.FIVE, Card.ACE],
            [Card.SIX, Card.ACE],
            [Card.ACE, Card.SEVEN],
            [Card.ACE, Card.EIGHT],
            [Card.ACE, Card.NINE],
        ]

        dealer = [
            Card.TWO, Card.THREE, Card.FOUR, Card.FIVE, Card.SIX,
            Card.SEVEN, Card.EIGHT, Card.NINE, Card.TEN, Card.ACE
        ]

        results = [
            [Play.HIT] * 10,
            [Play.HIT] * 10,
            [Play.HIT] * 10,
            [Play.HIT] * 10,
            [Play.HIT] * 10,
            [Play.STAND] * 7 + [Play.HIT] * 3,
            [Play.STAND] * 10,
            [Play.STAND] * 10,
        ]
        
        for i, h in enumerate(hands):
            for j, d in enumerate(dealer):
                self.assertEqual(test_func(h, d), results[i][j], f"Hand: {h}, Dealer: {d}")

    # def test_get_play_pair_with_double_and_double_after_split(self):
    #     """
    #     This only tests the deviations when DOUBLE AND DOUBLE AFTER SPLIT are allowed.
    #     test_get_play_pair_without_double_and_double_after_split contains all the possible outcomes.
    #     """
    #     test_func = self.service.get_play

    #     self.service.add_rule(Rule.ALLOW_DOUBLE)
    #     self.service.add_rule(Rule.ALLOW_DOUBLE_AFTER_SPLIT)

    #     hands = [
    #         [Card.TWO, Card.TWO],
    #         [Card.THREE, Card.THREE],
    #         [Card.FOUR, Card.FOUR],
    #         [Card.SIX, Card.SIX],
    #     ]

    #     dealer = [
    #         Card.TWO, Card.THREE, Card.FOUR, Card.FIVE, Card.SIX,
    #     ]

    #     results = [
    #         [Play.SPLIT] * 5,
    #         [Play.SPLIT] * 5,
    #         [Play.HIT] * 3 + [Play.SPLIT] * 2,
    #         [Play.SPLIT] * 5
    #     ]
        
    #     for i, h in enumerate(hands):
    #         for j, d in enumerate(dealer):
    #             self.assertEqual(test_func(h, d), results[i][j], f"Hand: {h}, Dealer: {d}")

    # def test_get_play_pair_with_double_only(self):
    #     """
    #     This only tests the deviations when DOUBLE is allowed.
    #     test_get_play_soft_without_double contains all the possible outcomes.
    #     """
    #     test_func = self.service.get_play

    #     self.service.add_rule(Rule.ALLOW_DOUBLE)

    #     hands = [
    #         [Card.FIVE, Card.FIVE],
    #     ]

    #     dealer = [
    #         Card.TWO, Card.THREE, Card.FOUR, Card.FIVE, Card.SIX,
    #         Card.SEVEN, Card.EIGHT, Card.NINE
    #     ]

    #     results = [
    #         [Play.DOUBLE] * 8,
    #     ]
        
    #     for i, h in enumerate(hands):
    #         for j, d in enumerate(dealer):
    #             self.assertEqual(test_func(h, d), results[i][j], f"Hand: {h}, Dealer: {d}")

    # def test_get_play_pair_without_double_and_double_after_split(self):
    #     test_func = self.service.get_play

    #     hands = [
    #         [Card.TWO, Card.TWO],
    #         [Card.THREE, Card.THREE],
    #         [Card.FOUR, Card.FOUR],
    #         [Card.FIVE, Card.FIVE],
    #         [Card.SIX, Card.SIX],
    #         [Card.SEVEN, Card.SEVEN],
    #         [Card.EIGHT, Card.EIGHT],
    #         [Card.NINE, Card.NINE],
    #         [Card.TEN, Card.TEN],
    #         [Card.ACE, Card.ACE],
    #     ]

    #     dealer = [
    #         Card.TWO, Card.THREE, Card.FOUR, Card.FIVE, Card.SIX,
    #         Card.SEVEN, Card.EIGHT, Card.NINE, Card.TEN, Card.ACE
    #     ]

    #     results = [
    #         [Play.HIT] * 2 + [Play.SPLIT] * 4 + [Play.HIT] * 4,
    #         [Play.HIT] * 2 + [Play.SPLIT] * 4 + [Play.HIT] * 4,
    #         [Play.HIT] * 3 + [Play.HIT] * 7,
    #         [Play.HIT] * 10,
    #         [Play.HIT] + [Play.SPLIT] * 4 + [Play.HIT] * 5,
    #         [Play.SPLIT] * 6 + [Play.HIT] * 4,
    #         [Play.SPLIT] * 10,
    #         [Play.SPLIT] * 5 + [Play.STAND] * 1 + [Play.SPLIT] * 2 + [Play.STAND] * 2,
    #         [Play.STAND] * 10,
    #         [Play.SPLIT] * 10,
    #     ]
        
    #     for i, h in enumerate(hands):
    #         for j, d in enumerate(dealer):
    #             self.assertEqual(test_func(h, d), results[i][j], f"Hand: {h}, Dealer: {d}")


if __name__ == "__main__":
    unittest.main()
